"""Quiz endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.quiz import (
    QuizCreate, QuizResponse, QuizQuestionResponse, 
    QuizSubmission, QuizResult, QuizHistoryResponse
)
from app.models.quiz import Quiz, QuizQuestion, QuizHistory
from app.models.course import Course, Chapter
from app.models.upload import Upload
from app.models.user import User
from app.auth import get_current_active_user
from app.services.genai_service import genai_service
from bson import ObjectId

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=dict)
async def generate_quiz(
    course_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    prompt: Optional[str] = None,
    num_questions: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Generate quiz from course, chapter, or prompt."""
    try:
        content = ""
        quiz_title = "Generated Quiz"
        
        if course_id:
            # Generate from course
            course = await Course.get(ObjectId(course_id))
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found"
                )
            
            chapters = await Chapter.find(Chapter.course_id == course.id).to_list()
            content = course.description + "\n\n"
            
            for chapter in chapters:
                content += f"Chapter {chapter.order}: {chapter.title}\n{chapter.content}\n\n"
            
            quiz_title = f"Quiz: {course.title}"
            
        elif chapter_id:
            # Generate from chapter
            chapter = await Chapter.get(ObjectId(chapter_id))
            if not chapter:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chapter not found"
                )
            
            content = chapter.content
            quiz_title = f"Quiz: {chapter.title}"
            
        elif prompt:
            # Generate from prompt
            content = prompt
            quiz_title = "Custom Quiz"
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either course_id, chapter_id, or prompt must be provided"
            )
        
        # Generate quiz questions using AI
        questions_data = await genai_service.generate_quiz_questions(content, num_questions)
        
        # Create quiz
        quiz = Quiz(
            course_id=ObjectId(course_id) if course_id else None,
            chapter_id=ObjectId(chapter_id) if chapter_id else None,
            title=quiz_title,
            prompt=prompt or f"AI-generated quiz from {'course' if course_id else 'chapter' if chapter_id else 'prompt'}"
        )
        await quiz.insert()
        
        # Create quiz questions
        questions = []
        for i, question_data in enumerate(questions_data):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=question_data["question"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data.get("explanation"),
                order=i + 1
            )
            await question.insert()
            questions.append(QuizQuestionResponse.model_validate(question))
        
        return {
            "quiz_id": str(quiz.id),
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )


@router.post("/manual", response_model=QuizResponse)
async def create_manual_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a manual quiz."""
    try:
        # Verify course exists
        course = await Course.get(ObjectId(quiz_data.course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verify chapter exists if provided
        if quiz_data.chapter_id:
            chapter = await Chapter.get(ObjectId(quiz_data.chapter_id))
            if not chapter or str(chapter.course_id) != quiz_data.course_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chapter not found"
                )
        
        # Create quiz
        quiz = Quiz(
            course_id=ObjectId(quiz_data.course_id),
            chapter_id=ObjectId(quiz_data.chapter_id) if quiz_data.chapter_id else None,
            title=quiz_data.title,
            prompt=quiz_data.prompt
        )
        
        await quiz.insert()
        
        return QuizResponse.model_validate(quiz)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course or chapter not found"
        )


@router.post("/", response_model=QuizResponse)
async def create_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new quiz."""
    try:
        # Verify course exists
        course = await Course.get(ObjectId(quiz_data.course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verify chapter exists if provided
        if quiz_data.chapter_id:
            chapter = await Chapter.get(ObjectId(quiz_data.chapter_id))
            if not chapter or str(chapter.course_id) != quiz_data.course_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chapter not found"
                )
        
        # Create quiz
        quiz = Quiz(
            course_id=ObjectId(quiz_data.course_id),
            chapter_id=ObjectId(quiz_data.chapter_id) if quiz_data.chapter_id else None,
            title=quiz_data.title,
            prompt=quiz_data.prompt
        )
        
        await quiz.insert()
        
        return QuizResponse.model_validate(quiz)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course or chapter not found"
        )


@router.post("/from-course/{course_id}", response_model=QuizResponse)
async def create_quiz_from_course(
    course_id: str,
    title: str,
    num_questions: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Create a quiz from course content using AI."""
    try:
        # Get course
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Get course content
        chapters = await Chapter.find(Chapter.course_id == course.id).to_list()
        content = course.description + "\n\n"
        
        for chapter in chapters:
            content += f"Chapter {chapter.order}: {chapter.title}\n{chapter.content}\n\n"
        
        # Generate quiz questions using AI
        questions_data = await genai_service.generate_quiz_questions(content, num_questions)
        
        # Create quiz
        quiz = Quiz(
            course_id=course.id,
            title=title,
            prompt=f"AI-generated quiz from course: {course.title}"
        )
        await quiz.insert()
        
        # Create quiz questions
        for i, question_data in enumerate(questions_data):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=question_data["question"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data.get("explanation"),
                order=i + 1
            )
            await question.insert()
        
        return QuizResponse.model_validate(quiz)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quiz from course: {str(e)}"
        )


@router.post("/from-upload/{upload_id}", response_model=QuizResponse)
async def create_quiz_from_upload(
    upload_id: str,
    title: str,
    num_questions: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Create a quiz from uploaded file content using AI."""
    try:
        # Get upload
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create quiz from this upload"
            )
        
        if not upload.extracted_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Upload has no extracted text content"
            )
        
        # Generate quiz questions using AI
        questions_data = await genai_service.generate_quiz_questions(
            upload.extracted_text, num_questions
        )
        
        # Create quiz
        quiz = Quiz(
            course_id=None,  # No course associated
            title=title,
            prompt=f"AI-generated quiz from upload: {upload.filename}"
        )
        await quiz.insert()
        
        # Create quiz questions
        for i, question_data in enumerate(questions_data):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=question_data["question"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data.get("explanation"),
                order=i + 1
            )
            await question.insert()
        
        return QuizResponse.model_validate(quiz)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create quiz from upload: {str(e)}"
        )


@router.get("/", response_model=List[QuizResponse])
async def get_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    course_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get quizzes."""
    query = {}
    if course_id:
        query["course_id"] = ObjectId(course_id)
    
    quizzes = await Quiz.find(query).skip(skip).limit(limit).sort("-created_at").to_list()
    return [QuizResponse.model_validate(quiz) for quiz in quizzes]


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific quiz."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        return QuizResponse.model_validate(quiz)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.get("/{quiz_id}/questions", response_model=List[QuizQuestionResponse])
async def get_quiz_questions(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get questions for a quiz."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        questions = await QuizQuestion.find(
            QuizQuestion.quiz_id == quiz.id
        ).sort("order").to_list()
        
        return [QuizQuestionResponse.model_validate(question) for question in questions]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(
    quiz_id: str,
    submission: QuizSubmission,
    current_user: User = Depends(get_current_active_user)
):
    """Submit quiz answers and get results."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Get quiz questions
        questions = await QuizQuestion.find(
            QuizQuestion.quiz_id == quiz.id
        ).sort("order").to_list()
        
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quiz has no questions"
            )
        
        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        answers = []
        
        for question in questions:
            user_answer = None
            for answer in submission.answers:
                if answer.get("question_id") == str(question.id):
                    user_answer = answer.get("answer")
                    break
            
            is_correct = user_answer == question.correct_answer
            if is_correct:
                correct_answers += 1
            
            answers.append({
                "question_id": str(question.id),
                "question": question.question,
                "user_answer": user_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation
            })
        
        score = (correct_answers / total_questions) * 100
        
        # Save quiz history
        quiz_history = QuizHistory(
            quiz_id=quiz.id,
            user_id=current_user.id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            answers=answers
        )
        await quiz_history.insert()
        
        return QuizResult(
            quiz_id=str(quiz.id),
            user_id=str(current_user.id),
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            answers=answers,
            taken_at=quiz_history.taken_at
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.get("/history", response_model=List[QuizHistoryResponse])
async def get_quiz_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's quiz history."""
    history = await QuizHistory.find(
        QuizHistory.user_id == current_user.id
    ).skip(skip).limit(limit).sort("-taken_at").to_list()
    
    return [QuizHistoryResponse.model_validate(record) for record in history]


@router.get("/history/{history_id}", response_model=QuizResult)
async def get_quiz_history_detail(
    history_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed quiz history."""
    try:
        history = await QuizHistory.get(ObjectId(history_id))
        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz history not found"
            )
        
        if history.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this quiz history"
            )
        
        return QuizResult(
            quiz_id=str(history.quiz_id),
            user_id=str(history.user_id),
            score=history.score,
            total_questions=history.total_questions,
            correct_answers=history.correct_answers,
            answers=history.answers,
            taken_at=history.taken_at
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz history not found"
        )


@router.patch("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: str,
    title: str = None,
    prompt: str = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update quiz."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Check if user owns the course
        course = await Course.get(quiz.course_id)
        if course and course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this quiz"
            )
        
        if title is not None:
            quiz.title = title
        if prompt is not None:
            quiz.prompt = prompt
        
        await quiz.save()
        return QuizResponse.model_validate(quiz)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete quiz."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Check if user owns the course
        course = await Course.get(quiz.course_id)
        if course and course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this quiz"
            )
        
        # Delete quiz questions
        await QuizQuestion.find(QuizQuestion.quiz_id == quiz.id).delete()
        
        # Delete quiz
        await quiz.delete()
        
        return {"message": "Quiz deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.post("/{quiz_id}/grade")
async def grade_quiz(
    quiz_id: str,
    answers: List[dict],
    current_user: User = Depends(get_current_active_user)
):
    """Grade quiz manually."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Get quiz questions
        questions = await QuizQuestion.find(
            QuizQuestion.quiz_id == quiz.id
        ).sort("order").to_list()
        
        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            if i < len(answers) and answers[i].get("answer") == question.correct_answer:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "score": score,
            "correct": correct_answers,
            "wrong": total_questions - correct_answers,
            "explanation": f"You got {correct_answers} out of {total_questions} questions correct."
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )


@router.get("/{quiz_id}/results")
async def get_quiz_results(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get quiz results."""
    try:
        quiz = await Quiz.get(ObjectId(quiz_id))
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        # Get user's quiz history for this quiz
        history = await QuizHistory.find(
            QuizHistory.quiz_id == quiz.id,
            QuizHistory.user_id == current_user.id
        ).sort("-taken_at").to_list()
        
        return [
            {
                "quiz_id": str(h.quiz_id),
                "score": h.score,
                "total_questions": h.total_questions,
                "correct_answers": h.correct_answers,
                "taken_at": h.taken_at
            }
            for h in history
        ]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
