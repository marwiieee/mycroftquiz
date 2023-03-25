from mycroft import MycroftSkill, intent_file_handler
import random

class QuizGameSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is the tallest mountain in the world?", "answer": "Mount Everest"},
            {"question": "What is the largest country in the world by area?", "answer": "Russia"},
        ]
        random.shuffle(self.questions)
        self.current_question_index = 0
        self.score = 0
        self.last_question = None

    @intent_file_handler('quiz_game.intent')
    def handle_quiz_game_intent(self, message):
        if self.current_question_index >= len(self.questions):
            self.speak('That was the last question. Your final score is {} out of {}.'.format(self.score, len(self.questions)))
            return
        current_question = self.questions[self.current_question_index]
        self.speak(current_question['question'])
        self.last_question = current_question
        self.current_question_index += 1

    @intent_file_handler('quiz_answer.intent')
    def handle_quiz_answer_intent(self, message):
        if self.current_question_index > len(self.questions):
            return
        current_question = self.questions[self.current_question_index - 1]
        user_answer = message.data.get('answer')
        if user_answer.lower() == current_question['answer'].lower():
            self.score += 1
            self.speak('Correct!')
        else:
            self.speak('Sorry, the correct answer was {}.'.format(current_question['answer']))

    @intent_file_handler('repeat_question.intent')
    def handle_repeat_question_intent(self, message):
        if self.last_question:
            self.speak(self.last_question['question'])
        else:
            self.speak('Sorry, there is no question to repeat.')

def create_skill():
    return QuizGameSkill()
