## Overview
This project is a Horoscope Generator API that provides daily horoscopes for all zodiac signs. The API is built with Flask (backend) and Streamlit (frontend), offering features to view, save, and manage your daily horoscopes.

## Features
* Daily Horoscope: Get today's horoscope for any zodiac sign

* Save Horoscopes: Save your favorite horoscopes for later viewing

* Manage Saved Horoscopes: View and delete previously saved horoscopes

* User-Friendly Interface: Clean and intuitive Streamlit web interface

## Technologies Used
* Backend: Flask (Python web framework), Langchain libraries and RAG

* Frontend: Streamlit (for interactive web interface)

* Database: SQLite (for storing saved horoscopes)

* Horoscope Data: Gemini API (or custom horoscope generation)

## Installation
* Prerequisites
* Python 3.7 or higher

pip (Python package manager)

## API Endpoints
* GET /horoscope/<sign> - Get today's horoscope for a specific zodiac sign

* POST /save_horoscope - Save a horoscope (requires JSON payload)

* GET /saved_horoscopes - Get all saved horoscopes

* DELETE /delete_horoscope/<id> - Delete a saved horoscope by ID
