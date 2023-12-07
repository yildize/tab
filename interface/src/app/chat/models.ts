export class Question {
    isFeedbackReceived = false;
    constructor(public sender:string, public user_question:string, public time_tag:string, public k?:number){}
    
    getMessageContent(){
      return this.user_question
    }
    
    get askData(){
      return {sender: this.sender, user_question:this.user_question, time_tag:this.time_tag}
    }
  }
  
  export class Answer {
    isFeedbackReceived = false;
    isLiked = false;
    suggested_answer = '';
    constructor(public sender:string, public user_question:string, 
                public time_tag:string, public answer:string, public extra_questions:ExtraQuestions, 
                public matched_question:string, public meta_data: MetaData, 
                public similarity:number,public k?:number){}
    
    getMessageContent(){
      return this.answer
    }
    
    get feedbackData(){
      return {is_liked:this.isLiked, user_question:this.user_question, matched_question:this.matched_question, matched_answer:this.answer, suggested_answer:this.suggested_answer}
    }
  }
  
  type ExtraQuestions = {
    questions: string[]
    similarities: number[]
  }
  
  type MetaData = {
    source_name: string,
    page: number,
  }