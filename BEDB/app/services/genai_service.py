"""Google GenAI service for AI-powered features."""

import google.generativeai as genai
from typing import List, Dict, Optional, Any
from app.config import settings
from app.models.chat import ChatMode


class GenAIService:
    """Service for Google GenAI integration."""
    
    def __init__(self):
        """Initialize GenAI service."""
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_course_outline(self, topic: str, level: str = "beginner") -> str:
        """Generate a course outline from a topic."""
        prompt = f"""
        Create a comprehensive course outline for the topic: "{topic}"
        Level: {level}
        
        Please provide:
        1. Course title
        2. Brief description
        3. Learning objectives
        4. Detailed chapter structure with titles and brief descriptions
        5. Estimated duration for each chapter
        
        Format the response in a clear, structured way suitable for an online learning platform.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate course outline: {str(e)}")
    
    async def extract_text_from_content(self, content: str) -> str:
        """Extract and clean text from uploaded content."""
        prompt = f"""
        Extract and clean the main text content from the following material.
        Remove any formatting artifacts, headers, footers, or irrelevant information.
        Focus on the educational content and structure it clearly.
        
        Content:
        {content}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to extract text: {str(e)}")
    
    async def generate_quiz_questions(self, content: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """Generate quiz questions from content."""
        prompt = f"""
        Generate {num_questions} multiple choice questions based on the following content.
        Each question should have 4 options (A, B, C, D) with only one correct answer.
        
        Content:
        {content}
        
        Return the questions in JSON format:
        [
            {{
                "question": "Question text here",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 0,
                "explanation": "Explanation for the correct answer"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse the JSON response
            import json
            questions = json.loads(response.text)
            return questions
        except Exception as e:
            raise Exception(f"Failed to generate quiz questions: {str(e)}")
    
    async def generate_flashcards(self, content: str, num_cards: int = 10) -> List[Dict[str, str]]:
        """Generate flashcards from content."""
        prompt = f"""
        Generate {num_cards} flashcards based on the following content.
        Each flashcard should have a clear question and a concise answer.
        
        Content:
        {content}
        
        Return the flashcards in JSON format:
        [
            {{
                "question": "Question text here",
                "answer": "Answer text here"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            import json
            flashcards = json.loads(response.text)
            return flashcards
        except Exception as e:
            raise Exception(f"Failed to generate flashcards: {str(e)}")
    
    async def generate_summary(self, content: str) -> str:
        """Generate a summary of the content."""
        prompt = f"""
        Create a comprehensive summary of the following content.
        Include the main points, key concepts, and important details.
        Keep it concise but informative.
        
        Content:
        {content}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    async def chat_with_context(
        self, 
        message: str, 
        context: Optional[str] = None, 
        mode: ChatMode = ChatMode.HYBRID
    ) -> str:
        """Chat with AI using optional context."""
        if mode == ChatMode.STRICT and not context:
            return "I can only answer questions based on the provided course material. Please upload or select a course first."
        
        if context:
            prompt = f"""
            Context (course material):
            {context}
            
            User question: {message}
            
            Please answer the user's question based on the provided context.
            If the question cannot be answered from the context, please say so clearly.
            """
        else:
            prompt = f"""
            User question: {message}
            
            Please provide a helpful and accurate answer to this question.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate chat response: {str(e)}")
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using Gemini."""
        try:
            # Note: This is a placeholder. Gemini Pro doesn't directly provide embeddings.
            # You might need to use a different model or service for embeddings.
            # For now, we'll return a mock embedding.
            return [0.0] * 768  # Standard embedding dimension
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")


# Global instance
genai_service = GenAIService()
