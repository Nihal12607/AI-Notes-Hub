import streamlit as st
from src.prompt import pt
from src.download import render_buttons

def final_prompt(text:str) -> str:
    f_prompt = f"""
        You are an expert professor, senior technical writer, curriculum designer, and exam setter.

        Your ONLY objective is to create the highest-quality exam cheat sheet possible from the uploaded document.

        ====================================================================
        CRITICAL INSTRUCTIONS
        ====================================================================

        1. Read and understand the ENTIRE document before writing anything.

        2. Do NOT begin generating until every section, chapter, heading,
        subheading, table, diagram description, note, warning, example,
        exercise, code block, formula, and appendix has been processed.

        3. Every major topic in the document must appear in the final cheat sheet.

        4. Give equal importance to all sections of the document.
        Do NOT bias the cheat sheet toward the beginning or end.

        5. Use ONLY information explicitly contained in the document.

        6. Never use outside knowledge.

        7. Never invent facts.

        8. Never guess.

        9. Never omit an important topic because it appears only once.

        10. If multiple sections explain the same concept,
        merge them into one concise version.

        11. Remove all filler.

        12. Remove unnecessary explanations.

        13. Preserve all technically important information.

        14. Optimize entirely for exam revision.

        15. If the document is very large,
        prioritize important concepts while still ensuring every major topic is represented.

        ====================================================================
        OUTPUT STYLE
        ====================================================================

        Write everything in clean Markdown.

        Use

        # ## ### headings

        Use Markdown tables whenever comparisons exist.

        Use bullet points instead of paragraphs.

        Bold important terms.

        Use inline code formatting for

        - keywords
        - commands
        - operators
        - syntax
        - function names
        - methods
        - class names
        - filenames

        Never write long paragraphs.

        Never repeat information.

        Every section should be easy to scan.

        ====================================================================
        CHEAT SHEET STRUCTURE
        ====================================================================

        # Title

        Generate a concise title.

        ---

        # 1. Core Concepts

        List every major concept.

        One bullet per concept.

        Maximum two lines.

        ---

        # 2. Important Definitions

        Create a table.

        | Term | Definition |

        Definitions should be concise.

        ---

        # 3. Syntax, Commands, Operators & Formulas

        Extract every important

        - syntax pattern
        - programming construct
        - formula
        - operator
        - command
        - function signature

        Use

        | Syntax | Purpose | Notes |

        Examples include

        - language syntax
        - CLI commands
        - mathematical formulas
        - APIs
        - programming keywords

        Omit if not applicable.

        ---

        # 4. Built-in Functions / APIs / Commands

        If the document contains functions,
        methods,
        commands,
        libraries,
        or APIs,

        create a dedicated table.

        Example

        | Function | Purpose | Example |

        ---

        # 5. Important Facts

        Only exam-worthy facts.

        No explanations.

        Bullet list.

        ---

        # 6. Comparisons

        Whenever two or more things are compared,

        convert them into Markdown tables.

        Examples

        Data structures

        Algorithms

        Functions

        Classes

        Keywords

        Operators

        Libraries

        Protocols

        Features

        Advantages

        Disadvantages

        Anything comparable.

        ---

        # 7. Workflows / Algorithms / Processes

        Convert every process into numbered steps.

        Never use paragraphs.

        Keep each step concise.

        ---

        # 8. Common Mistakes / Frequently Confused Concepts

        Extract mistakes students are likely to make.

        Create comparison tables whenever possible.

        Examples

        - `==` vs `is`
        - `append()` vs `extend()`
        - Stack vs Queue

        Only include concepts present in the document.

        ---

        # 9. Important Examples

        Extract only the BEST examples.

        Shorten them.

        Remove unnecessary code.

        Keep only the essential lines.

        Always use Markdown code blocks when showing code.

        ---

        # 10. Quick Reference Tables

        Create additional high-density reference tables whenever useful.

        Examples

        - Built-in functions
        - String methods
        - List methods
        - Dictionary methods
        - Operators
        - File modes
        - HTTP status codes
        - SQL commands
        - Linux commands

        Only include information found in the document.

        ---

        # 11. One-Page Revision Sheet

        THIS IS THE MOST IMPORTANT SECTION.

        Create an extremely dense revision sheet.

        Rules

        - Maximum information density
        - One bullet per concept
        - No explanations
        - No full paragraphs
        - Include syntax whenever useful
        - Include operators
        - Include commands
        - Include formulas
        - Include function names
        - Include keywords
        - Include tricky facts

        If the document is large,
        produce enough bullets to cover every major topic.

        ---

        # 12. Last-Minute Revision

        Generate 30–100 ultra-short memory triggers.

        Each bullet

        - under 10 words whenever possible
        - one fact only
        - bold important words

        Example

        • **Stack** → LIFO

        • **Queue** → FIFO

        • **finally** → Always executes

        • **dict.get()** → Safe lookup

        ====================================================================
        QUALITY CHECK (MANDATORY)
        ====================================================================

        Before returning the answer, silently verify:

        ✓ The ENTIRE document has been covered.

        ✓ Every major chapter appears.

        ✓ No important topic has been skipped.

        ✓ No hallucinated information exists.

        ✓ Similar information has been merged.

        ✓ Tables were used whenever appropriate.

        ✓ Code examples are minimal.

        ✓ Syntax uses inline code formatting.

        ✓ Methods use inline code formatting.

        ✓ Operators use inline code formatting.

        ✓ Commands use inline code formatting.

        ✓ Information density is maximized.

        ✓ Output is optimized for exam revision.

        If any check fails, improve the cheat sheet before returning it.

        ====================================================================
        DOCUMENT
        ====================================================================

        {text}
        """
    return f_prompt

text = st.session_state.get("pdf_notes")
if not text:
    st.switch_page("Home.py")


# Title
st.title("🧾Cheatsheet Generator")

# Output 

response = ""
with st.container(border=True):
    with st.spinner("🧠 Analyzing your Notes and Generating Content......"):
            response = pt(final_prompt(text))
    st.markdown(response)
render_buttons(response)