export class Question {
    isFeedbackReceived = false;
    constructor(public sender:string, public user_question:string, public time_tag:string, public k?:number){}
    
    getMessageContent(){
      return this.user_question
    }
    
    get askData(){
      return {sender:this.sender, user_question:this.user_question, time_tag:this.time_tag}
    }
  }
  
  export class Answer {
    isFeedbackReceived = false;
    isLiked = false;
    suggested_answer = '';
    ragButtonPressed = false;
    constructor(public sender:string, public user_question:string, 
                public time_tag:string, public answer:string, public extra_questions:ExtraQuestions, 
                public matched_question:string, public meta_data: MetaData, 
                public similarity:number,public k?:number){}
    
    getMessageContent(){
      return this.answer
    }
    
    get feedbackData(){
      return {is_rag: false, is_liked:this.isLiked, user_question:this.user_question, matched_question:this.matched_question, matched_answer:this.answer, suggested_answer:this.suggested_answer}
    }
  }

  export class RAGAnswer {
    isFeedbackReceived = false;
    isLiked = false;
    suggested_answer = '';
    chatHistoryAddIndex = -1;
    constructor(public sender:string, public user_question:string, 
                public time_tag:string, public answer:string,   
                public meta_data: MetaData[]){}
    
    getMessageContent(){
      return this.answer
    }
    
    get feedbackData(){
      return {is_rag: true, is_liked:this.isLiked, user_question:this.user_question, rag_answer:this.answer, suggested_answer:this.suggested_answer, sources:this.meta_data.map(data => `${data.source_name} [${data.page}]`).join(', ')}
    }
  }
  
  type ExtraQuestions = {
    questions: string[]
    similarities: number[]
  }
  
  export type MetaData = {
    source_name: string,
    page: number,
  }


// RAG Response

interface RetrievalInfo {
  q: string;
  dist: number;
  token_len: number;
  cross_encoder_score?: number; // Optional since it might not be present for some docs
}

export interface Metadata {
  source: string;
  page: number;
  retrieval_info?: RetrievalInfo; // '?' denotes an optional property
  answer?: string;
  doc_index?: number;
  page_summary?: string;
}

export interface RAGResponse {
  answer: string;
  metadata: Metadata[];
}


