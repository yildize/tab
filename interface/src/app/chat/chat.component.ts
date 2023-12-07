import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { Answer, Question } from './models';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements OnInit {
  @ViewChild('textareaElem') textAreaElement!: ElementRef;

  chatHistory: (Question | Answer)[] = [];
  userQuestionText: string = '';
  isWaitingForQuestionResponse: boolean = false;
  isWaitingForFeedbackResponse: boolean = false;
  selectedAnswer: any;
  displayDialog: boolean = false;
  questionAPIURL = environment.apiRootUrl + '/question';
  feedbackAPIURL = environment.apiRootUrl + '/feedback';
  doNotRespondConfidenceThreshold = environment.doNotRespondConfidenceThreshold;

  constructor(
    private http: HttpClient,
    private messageService: MessageService
  ) {}

  ngOnInit() {}

  sendWithEnter(event: Event): void {
    const keyboardEvent = event as KeyboardEvent;
    if (this.isUserQuestionValid) {
      this.onSendQuestion();
      keyboardEvent.preventDefault(); // Prevent the default "Enter" action
    }
  }

  onSendQuestion() {
    // Do not allow new question firing unless the response is arrived or something is typed.
    if (this.isWaitingForQuestionResponse || !this.isUserQuestionValid) return;

    let q = new Question('dummy_sender_name', this.userQuestionText, this.currentDate);
    this.pushToChatHistory(q);
    this.askQuestionToAPI(q);
  }

  askQuestionToAPI(q: Question) {
    this.http
      .post(this.questionAPIURL, q.askData)
      .subscribe({
        next: (response: any) => {
          console.log(response);
          let answer: Answer = this.responseToAnswer(response);
          this.pushToChatHistory(answer);
        },
        error: (error) => {
          this.errorToast(error.status);
          this.isWaitingForQuestionResponse = false;

          /*let answer: Answer = new Answer( "sender", "user_question", "time_tag",
            "This is the answer", {"questions":["q1", "q2"], "similarities":[0.2,0.4]}, "those are matched questions",
            {"source_name":"a source", page:7}, 0.7, 3
          );
          this.pushToChatHistory(answer)*/

        },
      });
  }

  pushToChatHistory(elm: Question | Answer) {
    if (elm instanceof Question) {
      this.chatHistory.push(elm);
      // After a new user question is pushed to the history we,
      this.userQuestionText = ''; // clean the text area
      this.textAreaManualAdjustment(); // adjust the text area height.
      this.isWaitingForQuestionResponse = true; // start waiting for the response
    }
    if (elm instanceof Answer) {
      if (elm.similarity < this.doNotRespondConfidenceThreshold) {
        elm.answer = "Sorry, I am not sure I understand the question."
      }
      this.chatHistory.push(elm);
      this.isWaitingForQuestionResponse = false;
    }
  }

  onLike(answer: Answer | Question) {
    if (this.isWaitingForFeedbackResponse) return;
    this.isWaitingForFeedbackResponse = true;

    this.http
      .post(this.feedbackAPIURL, (answer as Answer).feedbackData)
      .subscribe({
        next: (response: any) => {
          this.messageService.add({
            severity: 'info',
            summary: 'Like feedback received',
          });
          answer.isFeedbackReceived = true;
          this.isWaitingForFeedbackResponse = false;
        },
        error: (error) => {
          this.errorToast(error.status);
          answer.isFeedbackReceived = true;
          this.isWaitingForFeedbackResponse = false;
        },
      });
  }

  onDislike(answer: Answer | Question) {
    if (this.isWaitingForFeedbackResponse) return;
    this.isWaitingForFeedbackResponse = true;

    this.http
      .post(this.feedbackAPIURL, (answer as Answer).feedbackData)
      .subscribe({
        next: (response: any) => {
          this.messageService.add({
            severity: 'info',
            summary: 'Dislike feedback received',
          });
          answer.isFeedbackReceived = true;
          this.isWaitingForFeedbackResponse = false;
        },
        error: (error) => {
          this.errorToast(error.status);
          answer.isFeedbackReceived = true;
          this.isWaitingForFeedbackResponse = false;
        },
      });
  }

  onMore(answer: Answer | Question) {
    if (answer instanceof Answer) {
      this.selectedAnswer = {
        similarityScore: answer.similarity,
        matchedQuestion: answer.matched_question,
        source: answer.meta_data.source_name,
        page: answer.meta_data.page,
        time_tag: answer.time_tag,
        extra_questions: answer.extra_questions
      }
      this.displayDialog = true;
    }
  }

  responseToAnswer(response: any): Answer {
    return new Answer( response.sender, response.user_question, response.time_tag,
      response.answer, response.extra_questions, response.matched_question,
      response.meta_data, response.similarity, response.k
    );
  }

  get isUserQuestionValid(){
    return this.userQuestionText.trim()!== ''
  }

  get currentDate() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}T${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
  }
  
  errorToast(errorStatus: number) {
    this.messageService.add({
      severity: 'error',
      summary: 'Error',
      detail: 'There was an error processing the request. Code: ' + errorStatus,
    });
  }

  textAreaManualAdjustment() {
    this.textAreaElement.nativeElement.value = '';
    this.adjustHeight({ target: this.textAreaElement.nativeElement });
  }

  adjustHeight(event: any): void {
    const textarea = event.target as HTMLElement;
    textarea.style.height = 'auto';
    if (textarea.scrollHeight > 120) {
      // Shows vertical scrollbar if textarea content is large
      textarea.style.overflow = 'auto';
    } else {
      // Hides scrollbar if content is small
      textarea.style.overflow = 'hidden';
    }
    textarea.style.height = textarea.scrollHeight + 'px';

    // Adjust chat container height based on input container height
    const inputContainer = document.querySelector('.input-container') as HTMLElement;
    const inputContainerHeight = inputContainer.offsetHeight;
    const chatContainer = document.querySelector('.chat-container') as HTMLElement;
    chatContainer.style.paddingBottom = inputContainerHeight + 'px';
  }

  isElmQuestion(elm: Question | Answer) {
    return elm instanceof Question;
  }

  isElmAnswer(elm: Question | Answer) {
    return elm instanceof Answer;
  }

}