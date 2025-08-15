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

    # model = genai.GenerativeModel("gemini-pro-vision")
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
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
                   page_icon="💊",
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

# Main content.
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
    st.image("pic.png", use_container_width=True)  # Add your logo here for branding
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
    
    Your expertise is required to identify a drug and extract concise, clinically accurate details.
    
    Task: For a given drug, produce a compact authoritative summary (≤150 words) with short headers (1–2 lines each). Be clinical, precise, and suitable for healthcare professionals.
    
    Required headings:
    • Drug name (generic ± common brand)
    • Active ingredient(s)
    • Indications / therapeutic use
    • Typical dose & route
    • Common side effects
    • Serious / rare adverse effects
    • Contraindications & key precautions
    • Major drug interactions / monitoring
    
    Accuracy: Prioritize reliable, unambiguous language. Keep entries brief, fact-focused, and ready for professional use.
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











# import streamlit as st
# import os
# import google.generativeai as genai
# import time
# from dotenv import load_dotenv


# # Load environment variables
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     st.error("Missing GOOGLE_API_KEY in environment")
#     st.stop()

# # Configure Generative AI API
# os.environ['GOOGLE_API_KEY'] = api_key
# genai.configure(api_key=api_key)


# def image_to_part(uploaded_image):
#     """
#     Convert a Streamlit UploadedFile into a genai.Part for images.
#     """
#     if uploaded_image is None:
#         return None
#     raw = uploaded_image.getvalue()
#     # genai.Part.from_bytes handles any binary blob (image/audio/etc.) with a mime_type
#     return genai.Part.from_bytes(raw, mime_type=uploaded_image.type)


# def get_gemini_response(user_text: str, uploaded_image, system_prompt: str) -> str:
#     """
#     Call Gemini Pro Vision with the user text, uploaded image, and system prompt.
#     Returns the generated text wrapped in Markdown fences.
#     """
#     # Safety settings to disable all blocking thresholds
#     safety_settings = [
#         {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
#         {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
#         {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
#     ]

#     # Instantiate the vision-capable model
#     model = genai.GenerativeModel("gemini-pro-vision")

#     # Wrap each piece of content in a Part
#     parts = [
#         genai.Part.from_text(user_text),
#         image_to_part(uploaded_image),
#         genai.Part.from_text(system_prompt)
#     ]

#     # Generate the response
#     response = model.generate_content(parts, safety_settings=safety_settings)
#     return f"```markdown\n{response.text}\n```"



# # ---------------- Streamlit UI ---------------- #

# # Page config & styling
# st.set_page_config(
#     page_title="Med Assistance AI",
#     page_icon="💊",
#     layout="centered"
# )
# st.markdown("""
#     <style>
#       body { background: linear-gradient(to right, #ff7e5f, #feb47b); font-family: Arial, sans-serif; }
#       .separator { margin: 20px 0; height: 2px; background-color: #ddd; }
#     </style>
# """, unsafe_allow_html=True)

# # Main header
# st.markdown("# Med Assistance AI by Stanlito")
# st.markdown(
#     "Upload a photo of a medication and ask any question about it. "
#     "Our AI will analyze the image and provide detailed information on its composition, usage, side effects, and precautions."
# )

# # Sidebar
# st.sidebar.image("pic.png", use_container_width=True)
# st.sidebar.header("About Med Assistance")
# st.sidebar.markdown(
#     "Med Assistance AI empowers you with clear, reliable insights into pharmaceuticals. "
#     "Whether you’re a researcher, healthcare professional, or simply curious, "
#     "get the knowledge you need at your fingertips."
# )

# st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# # User inputs
# input_text = st.text_input(
#     "What information do you seek about this drug?",
#     placeholder="e.g. active ingredients, side effects, usage guidelines..."
# )
# uploaded_image = st.file_uploader(
#     "Upload a photo of the drug:",
#     type=["jpg", "jpeg", "png"]
# )

# submit = st.button("Describe the Product")

# # System prompt for the AI
# system_prompt = """
# Welcome to Drug Information Extraction Task.

# Your task is to provide comprehensive information about any drug.

# You will identify the drug and extract key details such as:
# - Drug name
# - Active ingredients
# - Therapeutic uses
# - Potential side effects
# - Contraindications and precautions

# Provide clear, accurate, and concise summaries for each aspect.
# """

# # Handle the submission
# if submit:
#     if not input_text or not uploaded_image:
#         st.error("Please upload an image *and* enter your question.")
#     else:
#         with st.spinner("Analyzing image and generating response..."):
#             start_time = time.time()
#             markdown_response = get_gemini_response(input_text, uploaded_image, system_prompt)
#             elapsed = time.time() - start_time

#         st.subheader("Analysis Result")
#         st.markdown(markdown_response)
#         st.caption(f"Response generated in {elapsed:.2f} seconds")
