from flask import Flask, request, render_template
from openai import OpenAI
import os

app = Flask(__name__)

openai = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

conversation = []

@app.route('/')
def home():
    return render_template('index.html') #render_template is to redirect to index.html

@app.route('/predict',methods=['POST'])
def predict():

    inputs = [str(x) for x in request.form.values()]
    # content_type, market_segment, keyword, location
    promt = f"Write an SEO-optimized related only to IOT Water leak products {inputs[0]} targeting the {inputs[1]} market using the keyword '{inputs[2]}' and location '{inputs[3]}'. Ensure the content is relevant, how it can help, engaging, informative, and includes relevant headers."
    
    message = {
        "role": "user",
        "content": promt
    }
    conversation.append(message)

    response = openai.chat.completions.create(
        messages=conversation,
        model="gpt-3.5-turbo"
    )

    conversation.append(response.choices[0].message)

    output = response.choices[0].message.content

    print(output)

    return render_template('sample.html', generated_text=format(output))

if __name__ == "__main__":
    app.run(debug=True)