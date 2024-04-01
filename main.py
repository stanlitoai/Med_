import streamlit as st
import os
import base64
import google.generativeai as genai
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Set up Google API key
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Configure generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image, prompt):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        }
    ]

    model = genai.GenerativeModel("gemini-pro-vision")
    # model = model.start_chat(history=[])
    response = model.generate_content([input_text, image[0], prompt], safety_settings=safety_settings)
    # return response.text
    # Wrap the generated text in Markdown syntax
    markdown_response = f"```markdown\n{response.text}\n```"

    return markdown_response


def input_image_setup(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_image.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("Can't read uploaded image.")


# Initialize Streamlit app
st.set_page_config(page_title="Med Assistance App",
                   page_icon=":art:",
                   layout="centered",
                   initial_sidebar_state="auto")

# Custom CSS for gradient background and centering content
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ff7e5f, #feb47b); /* Gradient from pink to orange */
        font-family: Arial, sans-serif;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .title {
        color: #fff; /* White color */
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center; /* Center the text */
    }
    .subtitle {
        color: #fff; /* White color */
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center; /* Center the text */
    }
    </style>
    """, unsafe_allow_html=True)

# Main content
with st.container() as container:
    with st.container() as content:
        # Updated title
        st.markdown("# Med Assistance AI")
        st.markdown("Welcome to Drug Recognition AI, your ultimate companion in pharmaceutical knowledge. With a "
                    "simple snapshot, our AI scans and analyzes drugs, providing you with comprehensive insights into "
                    "their composition, usage, and potential effects. From detailed descriptions to safety "
                    "considerations, empower yourself with the information you need for informed decisions. Discover "
                    "the power of Drug Recognition AI today!")

# Sidebar
# Revised sidebar content
st.sidebar.header("Med Assistance AI")

with st.sidebar:
    st.image("pic.png", use_column_width=True)  # Add your logo here for branding
    st.markdown(
        """
        ## Welcome to Med Assistance
        Welcome to Med Assistance! We're here to simplify your journey through pharmaceuticals. Our AI platform offers insightful summaries and analyses of medications and their components. Whether you're a researcher, healthcare professional, or curious individual, empower your decisions with confidence using our precise insights.
        """
    )

# Separator with improved styling
st.markdown(
    """
    <style>
    .separator {
        margin-top: 20px;
        margin-bottom: 20px;
        height: 3px;
        background-color: #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# Input area
input_text = st.text_input(
    label="What information do you seek about this drug?",
    placeholder="Enter drug details or ask questions...",
    key="drug_input",
    help="Please provide details or ask questions about the drug to receive comprehensive insights."
)


# Image uploader
uploaded_image = st.file_uploader("Select an image...",
                                  type=["jpg", "jpeg", "png"],
                                  help=r"Click the `Browse files` to upload an image of your choice.")

# Display uploaded image
if uploaded_image is not None:
    image_data = base64.b64encode(uploaded_image.read()).decode()
    st.markdown(
        f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{image_data}" '
        f'alt="Uploaded Image" style="width: 60%; height: auto; max-width: 600px; border-radius: 10%; '
        f'border: 10px solid #ff7f0e;"></div>',
        unsafe_allow_html=True
    )

# Button to trigger description generation
submit_button = st.button("Describe the Product")

# Predefined prompt
input_prompt = """
    Welcome to Drug Information Extraction Task.

    Your task is to provide comprehensive information about any drug.
    
    Your expertise is crucial in accurately identifying the drug and extracting key details, such as its composition, 
    usage, side effects, and precautions.
    
    Your tasks is :
     Provide details about the drug's name, active ingredients, therapeutic uses, potential side effects, 
     and contraindications. Offer detailed explanations or summaries for each aspect.
    
    Ensure accuracy and precision in your information retrieval process to provide reliable insights to users.
    
    Your goal is to create a comprehensive summary covering all essential aspects of the drug.
    
   """

# Handle button click event
if submit_button:
    if uploaded_image and input_text:
        with st.spinner("Scanning your product and generating description..."):
            start = time.time()
            image_data = input_image_setup(uploaded_image)
            response = get_gemini_response(input_text, image_data, input_prompt)
            st.subheader("HELLO \n Here is the solution:")
            st.markdown(response)
            end = time.time()
    elif uploaded_image and not input_text:
        st.error("Please enter your prompt details before describing the product.")
    elif input_text and not uploaded_image:
        st.error("Please upload your product image before describing the product.")
    else:
        st.error("Please upload your product image and prompt details before describing the product.")
