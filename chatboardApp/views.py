import json
from django.shortcuts import render
import google.generativeai as genai
# from google import genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)
# client = genai.Client(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash") # Selects Gemini model

@csrf_exempt
def chat_with_ai(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Converts JSON request body into Python dictionary
            user_msg = data.get("message")

            if not user_msg:
                return JsonResponse({"reply": "Please type something."}, status=400)

            response = model.generate_content(user_msg)

            ai_reply = response.text

            print("AI REPLY:", ai_reply)

            return JsonResponse({"reply": ai_reply})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"reply": "Service is temporarily unavailable."}, status=500)

    return render(request, "chat.html")
