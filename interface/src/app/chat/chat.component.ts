import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { Answer, Question, RAGAnswer, RAGResponse, MetaData, Metadata } from './models';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements OnInit {
  @ViewChild('textareaElem') textAreaElement!: ElementRef;

  chatHistory: (Question | Answer | RAGAnswer)[] = [];
  userQuestionText: string = '';
  isWaitingForQuestionResponse: boolean = false;
  isWaitingForFeedbackResponse: boolean = false;
  isWaitingForRAGResponse: boolean = false;
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
  onSimilarQuestionClick(q:string){
    this.userQuestionText = q
    this.onSendQuestion()
    this.displayDialog = false;
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

  pushToChatHistory(elm: Question | Answer | RAGAnswer) {
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
    if (elm instanceof RAGAnswer){
      if (elm.chatHistoryAddIndex !== 0){
        this.chatHistory.splice(elm.chatHistoryAddIndex, 0, elm);
      }
      this.isWaitingForRAGResponse = true;
    }
  }

  onLike(answer: Answer | Question | RAGAnswer) {
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
          answer.isFeedbackReceived = false;
          this.isWaitingForFeedbackResponse = false;
        },
      });
  }

  onDislike(answer: Answer | Question | RAGAnswer) {
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
          answer.isFeedbackReceived = false;
          this.isWaitingForFeedbackResponse = false;
        },
      });
  }

  onMore(answer: Answer | Question | RAGAnswer) {
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

    if (answer instanceof RAGAnswer) {
      this.selectedAnswer = {
        sourcesAndPages: answer.meta_data.map(item => ({ source_name: item.source_name, page: item.page })),
        time_tag: answer.time_tag,
      }
      this.displayDialog = true;
    }
  }

  onRAG(answer: Answer | Question | RAGAnswer) {
    if (answer instanceof Answer) {
      answer.ragButtonPressed = true


      // create a dummy answer with loading animation
      let dummy_rag_answer: RAGAnswer = new RAGAnswer(answer.sender, answer.user_question, this.currentDate,
              "",  [{"source_name":"filler", page:0}]
      );
      const answerIndex = this.chatHistory.findIndex(element => element === answer);
      dummy_rag_answer.chatHistoryAddIndex = answerIndex+1
      this.pushToChatHistory(dummy_rag_answer)
      

      // Mimic the RAG request-response here
      setTimeout(() => {
        let dummy_response = {"answer":"Example RAG answer.", "metadata":[{"source":"source1.pdf", "page":0, "doc_index":111},
                                                                          {"source":"source2.pdf", "page":1, "doc_index":111},
                                                                          {"source":"source3.pdf", "page":2, "doc_index":111},
                                                                          {"source":"source4.pdf", "page":3, "doc_index":111},
                                                                          {"source":"source5.pdf", "page":4, "doc_index":111}
        ]}

      const [a, m] = this.extractRAGResponse(dummy_response)
      dummy_rag_answer.answer = a;
      dummy_rag_answer.meta_data = m

      this.isWaitingForRAGResponse = false;
      }, 10000);

      // send a request to RAG API
      // parse the response
      // update the dummy answer content

    }
  }

  extractRAGResponse(response:RAGResponse): [string, MetaData[]]{
    // Extract the answer directly
    const answer = response.answer;
    const metaDataList: MetaData[] = this.convertMetadata(response.metadata);
    return [answer, metaDataList]
  }

  convertMetadata(metadataArray: Metadata[]): MetaData[] {
    return metadataArray.map((item): MetaData => ({
      source_name: item.source,
      page: item.page
    }));
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

  isElmQuestion(elm: Question | Answer | RAGAnswer) {
    return elm instanceof Question;
  }

  isElmAnswer(elm: Question | Answer | RAGAnswer) {
    return elm instanceof Answer;
  }

  isElmRAGAnswer(elm: Question | Answer | RAGAnswer) {
    return elm instanceof RAGAnswer;
  }

  isRAGButtonPressed(elm: Question | Answer | RAGAnswer) {
    if (elm instanceof Answer){
      return elm.ragButtonPressed
    }
    return false
  }

}