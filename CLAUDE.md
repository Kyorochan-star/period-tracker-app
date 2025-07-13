# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Period Tracker application with:
- **Backend**: FastAPI (Python) REST API with SQLite database
- **Frontend**: Native iOS app using SwiftUI
- **Purpose**: Track menstrual cycles with AI-powered chat support featuring 5 personality modes

## Development Commands

### Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with required environment variables:
# DATABASE_URL=sqlite:///./backend.db
# JWT_SECRET=your-secret-key
# OPENAI_API_KEY=your-openai-key
# GOOGLE_CLIENT_ID=your-google-client-id

# Run the development server
uvicorn main:app --reload

# The API will be available at http://127.0.0.1:8000
# Swagger documentation at http://127.0.0.1:8000/docs
```

### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Open in Xcode
open PeriodTracker.xcodeproj

# Build and run:
# - Select target device/simulator
# - Press Cmd+R or click Run button
# - Requires Xcode 16.4+ and iOS 18.0+
```

## Architecture Overview

### Backend Architecture

The backend uses FastAPI with a layered architecture:

1. **Entry Point**: `main.py` - FastAPI app initialization, CORS setup, router inclusion
2. **Database Layer**: `database.py` - SQLAlchemy models:
   - `User`: Authentication with local/Google providers
   - `Period`: Menstrual cycle records with predictions
   - `ChatMessage`: AI conversation history
   - `PasswordResetToken`: Secure password reset
3. **API Layer**: `routers/` - Endpoint definitions:
   - `auth.py`: Login, register, Google OAuth, password reset
   - `periods.py`: CRUD operations for period tracking
   - `chat.py`: AI chat with personality modes
4. **Business Logic**: `crud.py` - Database operations
5. **Data Validation**: `schemas.py` - Pydantic models for request/response validation

### Frontend Architecture

The iOS app follows MVVM pattern with repository abstraction:

1. **App Structure**:
   - `PeriodTrackerApp.swift`: App entry point
   - `ContentView.swift`: Main tab navigation container
   
2. **Core Layer** (`Core/`):
   - **Models**: Domain models and DTOs for API communication
   - **Network**: `APIService.swift` handles all HTTP requests to backend
   - **Repositories**: Abstract data access with Mock and Network implementations
   
3. **Features Layer** (`Features/`):
   - **Auth**: Login, signup, password reset with `LoginViewModel.swift`
   - **Home**: Calendar view, period recording
   - **Chat**: AI chat with mode selection (5 personalities)
   - **Setting**: User profile and app settings

4. **Mock System**:
   - `MockData/`: JSON responses for offline development
   - Mock repositories for testing without backend

### Key Integration Points

1. **API Communication**:
   - Base URL configured in `frontend/PeriodTracker/Core/Network/APIConfig.swift`
   - Currently set to `http://127.0.0.1:8000`
   - All API calls go through `APIService` class

2. **Authentication Flow**:
   - JWT tokens stored in iOS app
   - Token included in Authorization header for protected endpoints
   - Support for both local and Google OAuth authentication

3. **Chat AI Integration**:
   - Backend uses OpenAI GPT-4 via `openai` library
   - 5 personality modes with system prompts in Japanese
   - Context includes user's period status for personalized responses

## Git Workflow

Follow the branching convention from README.md:
- Branch format: `{area}/{purpose}/{content}`
- Areas: `fe` (frontend), `be` (backend), `doc` (documentation)
- Purposes: `feat` (feature), `fix` (bug fix), `chore` (other)
- Example: `fe/feat/chat-ui`, `be/fix/auth`

Commit message format: `{purpose}: description`
- Example: `feat: チャットUIの修正`

## Current Development Focus

Based on the current branch (`fe/feat/fixfe-be`) and modified files, the team is working on:
- Frontend-backend integration fixes
- Authentication flow improvements
- API service updates in repositories
- User DTO and network layer enhancements

## Testing Note

Currently, the project lacks automated testing infrastructure. Testing is done through:
- Manual API testing via `testapiView.swift` in frontend
- Mock server (`frontend/test.py`) for frontend development
- Swagger UI for backend API testing