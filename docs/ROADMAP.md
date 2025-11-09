# DominoFit Solver - Project Roadmap

## Vision

Transform this tool from a basic puzzle solver into a comprehensive DominoFit puzzle assistant with AI-powered screenshot processing, enhanced UI, and robust architecture.

## Current State (v0.1.0)

### What Works
- ✅ Web-based UI for puzzle input
- ✅ Google OR-Tools constraint solver
- ✅ SVG generation of solutions
- ✅ Support for custom board sizes and blocked cells
- ✅ Row/column constraint validation

### Current Limitations
- Single-user only (global board state)
- Basic UI doesn't match game aesthetic
- Manual puzzle input only
- No multiple solution enumeration
- No puzzle generation
- No session persistence

## Development Phases

### Phase 1: Clean Up & Polish (Current)
**Goal**: Solid foundation for future development

- [x] Organize project structure
- [x] Add comprehensive documentation (CLAUDE.md, ROADMAP.md)
- [x] Fix VS Code configuration files
- [x] Update pyproject.toml with proper metadata
- [ ] Add .gitignore for Python/Flask projects
- [ ] Add requirements.txt for alternative installation
- [ ] Code cleanup and consistent formatting

### Phase 2: UI/UX Improvements
**Goal**: Match game aesthetic and improve usability

**High Priority**
- [ ] Size selector buttons (6×6, 7×7, 8×8) at top of page
- [ ] Display constraints on all 4 sides (top/bottom for columns, left/right for rows)
- [ ] Improved SVG rendering
  - Thicker domino borders (3-4px instead of 1px)
  - Match game color scheme (blue/purple constraint numbers)
  - Better dot positioning and sizing
  - Proper gray shading for blocked cells

**Medium Priority**
- [ ] Quick preset buttons for common board sizes
- [ ] Better constraint input UI (click edges to set values)
- [ ] Visual feedback for valid/invalid configurations
- [ ] Responsive mobile-friendly layout
- [ ] Dark mode support

**Low Priority**
- [ ] Animation of solution placement
- [ ] Keyboard shortcuts
- [ ] Accessibility improvements (ARIA labels, keyboard navigation)

### Phase 3: Enhanced Solver Features
**Goal**: More powerful solving capabilities

- [ ] Multiple solution enumeration
  - "Find all solutions" mode
  - "Count total solutions" for uniqueness validation
  - "Next solution" button to cycle through alternatives
- [ ] Solution statistics
  - Solve time
  - Number of solutions
  - Puzzle difficulty estimate
- [ ] Better error handling and user feedback
  - "No solution exists" with explanation
  - Parity check (odd free cells = impossible)
  - Constraint impossibility detection
- [ ] Export options
  - JSON format for puzzle sharing
  - PNG export (in addition to SVG)
  - Solution sharing via URL

### Phase 4: Screenshot-to-Puzzle (AI Integration)
**Goal**: Use local LLM to extract puzzles from screenshots

This is the most exciting feature - allowing users to simply screenshot a puzzle and have it automatically solved.

#### Architecture Decision: Multi-Project Structure

Since Ollama services require more complex infrastructure, this phase transitions to a **multi-project architecture**:

```
dominofit-suite/
├── dominofit-backend/      # Python FastAPI backend
│   ├── api/                # REST API endpoints
│   ├── solver/             # OR-Tools solver (migrated from current code)
│   ├── vision/             # LLM integration for screenshot processing
│   └── models/             # Data models
├── dominofit-frontend/     # Modern frontend (React/Vue/Svelte)
│   ├── components/         # UI components
│   └── assets/             # Static assets
└── dominofit-legacy/       # Current Flask app (for reference/fallback)
```

#### LLM Integration Options

**Option 1: Ollama with Vision Models (Recommended)**

Best models for this task:
- `llama3.2-vision:11b` - Most accurate, good for production
- `llava:7b` - Balanced speed/accuracy
- `moondream:1.8b` - Fast prototyping, surprisingly good

**Pros:**
- Fully local, no API costs, privacy-friendly
- Can handle variations (rotated images, partial screenshots, different layouts)
- Easy to set up and iterate

**Cons:**
- Requires decent GPU (recommend 8GB+ VRAM for 11B models)
- Slower than traditional CV (2-5 seconds per image)
- May occasionally hallucinate numbers

**Implementation:**
```python
import ollama
import json

def extract_puzzle_from_screenshot(image_path):
    """Extract puzzle constraints from screenshot using local LLM."""
    response = ollama.chat(
        model='llama3.2-vision:11b',
        messages=[{
            'role': 'user',
            'content': '''Analyze this DominoFit puzzle screenshot and extract:

            Return ONLY valid JSON (no markdown, no explanation):
            {
                "board_size": "8x8",
                "row_constraints": [8, 6, 5, 4, 5, 7, 5, 6],
                "col_constraints": [2, 6, 5, 7, 4, 6, 4, 12],
                "blocked_cells": [[0,1], [1,1], [2,0], ...]
            }

            Row constraints are the numbers on LEFT and RIGHT edges.
            Column constraints are the numbers on TOP and BOTTOM edges.
            Blocked cells are dark gray squares.
            Empty cells are light gray.
            ''',
            'images': [image_path]
        }]
    )

    # Parse JSON from LLM response
    data = json.loads(response['message']['content'])

    # Validate and convert to Board object
    board = validate_and_create_board(data)
    return board
```

**Option 2: Traditional Computer Vision (More Reliable)**

For highly structured screenshots with consistent format:
- OpenCV for grid detection
- Tesseract OCR for number extraction
- Template matching for blocked cells

**Pros:**
- Fast (< 1 second)
- More accurate for numbers (no hallucination)
- No GPU required
- Deterministic results

**Cons:**
- Brittle - breaks on rotated/cropped images
- Requires careful tuning for different screen sizes
- Can't handle game UI variations

**Option 3: Hybrid Approach (Best of Both Worlds)**

1. Use OpenCV to detect grid structure and cells
2. Use vision LLM to read just the constraint numbers
3. Fast and robust

#### API Design for Screenshot Processing

**Backend Endpoints:**
```
POST /api/puzzle/from-screenshot
  - Input: multipart/form-data with image file
  - Output: { board: {...}, confidence: 0.95 }
  - Process: LLM extraction + validation

GET /api/puzzle/{id}/solve
  - Input: puzzle_id
  - Output: { solution: [[...]], solve_time_ms: 150 }

POST /api/puzzle/validate
  - Input: { board: {...} }
  - Output: { valid: true, message: "..." }
```

#### Features for Screenshot Processing
- [ ] Ollama integration and model management
- [ ] Screenshot upload endpoint
- [ ] Puzzle extraction with confidence scoring
- [ ] Manual correction UI for misread values
- [ ] Side-by-side view: screenshot vs extracted puzzle
- [ ] Batch processing for multiple puzzles
- [ ] Auto-solve after extraction

#### Hardware Requirements
- **Minimum**: 8GB RAM, integrated GPU (for moondream)
- **Recommended**: 16GB RAM, 8GB+ VRAM GPU (for llama3.2-vision:11b)
- **Storage**: ~7GB per model (download once)

### Phase 5: Backend Architecture Refactor
**Goal**: Prepare for multi-user, API-driven architecture

**Migration to FastAPI**
- [ ] Convert Flask routes to FastAPI
- [ ] Add proper API documentation (OpenAPI/Swagger)
- [ ] Session management with Redis or database
- [ ] User authentication (optional)
- [ ] Rate limiting for solver endpoints

**Database Integration**
- [ ] Store puzzles and solutions
- [ ] User session management
- [ ] Puzzle library/collection

**Containerization**
- [ ] Dockerfile for backend
- [ ] Docker Compose for full stack
- [ ] Ollama container configuration

### Phase 6: Advanced Features
**Goal**: Power user features and community engagement

- [ ] Puzzle Generation
  - Generate valid puzzles with unique solutions
  - Difficulty rating algorithm
  - Constraint satisfaction for balanced puzzles
- [ ] Daily Puzzle
  - Auto-generate daily challenge
  - Leaderboard for solve times
- [ ] Puzzle Sharing
  - Generate shareable URLs
  - QR codes for puzzles
  - Community puzzle repository
- [ ] Statistics & Analytics
  - Solve time tracking
  - Success rate by difficulty
  - Personal stats dashboard
- [ ] Hint System
  - Suggest next valid placement
  - Highlight contradictions
  - Progressive hints (don't give it away)

### Phase 7: Mobile & Desktop Apps
**Goal**: Native applications for better UX

- [ ] Progressive Web App (PWA)
- [ ] Electron desktop app
- [ ] Mobile apps (React Native or Flutter)
- [ ] Offline mode

## Technical Debt & Improvements

### Code Quality
- [ ] Add type hints throughout
- [ ] Unit tests for solver logic
- [ ] Integration tests for API endpoints
- [ ] Code coverage reporting
- [ ] Linting and formatting (black, flake8, mypy)

### Performance
- [ ] Solver optimization for large boards
- [ ] Solution caching
- [ ] Lazy loading for UI
- [ ] SVG optimization

### Security
- [ ] Input validation and sanitization
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Secure file upload handling

## Timeline Estimates

| Phase | Estimated Time | Priority |
|-------|----------------|----------|
| Phase 1: Clean Up | 1-2 days | **High** |
| Phase 2: UI/UX | 1-2 weeks | **High** |
| Phase 3: Enhanced Solver | 1 week | Medium |
| Phase 4: Screenshot AI | 2-3 weeks | **High** |
| Phase 5: Backend Refactor | 2-3 weeks | Medium |
| Phase 6: Advanced Features | 3-4 weeks | Low |
| Phase 7: Mobile/Desktop | 1-2 months | Low |

## Success Metrics

- [ ] Solve time < 1 second for 8×8 puzzles
- [ ] Screenshot extraction accuracy > 95%
- [ ] Support for 100+ concurrent users
- [ ] UI matches game aesthetic (user testing)
- [ ] Comprehensive test coverage (>80%)

## Open Questions

1. Should we support puzzle creation/editing in the UI?
2. What's the right balance between local LLM accuracy and speed?
3. Do we need cloud deployment or is local-first sufficient?
4. Should we add social features (sharing, comments, likes)?
5. Is there value in a browser extension for instant puzzle solving?

## Contributing

This project is currently in active development. Future contributors should:
1. Read CLAUDE.md for project context
2. Follow existing code style and patterns
3. Add tests for new features
4. Update documentation

## Resources

- DominoFit Game: https://dominofit.isotropic.us/
- Google OR-Tools Docs: https://developers.google.com/optimization
- Ollama Documentation: https://ollama.ai/docs
- llama3.2-vision Model: https://ollama.ai/library/llama3.2-vision

---

Last Updated: 2025-11-09
Version: 0.1.0
