# LinkedIn Automation Platform - Complete Documentation

## 📋 Project Overview

The LinkedIn Automation Platform is a comprehensive full-stack investor discovery and contact enrichment system that combines multiple AI providers, web scraping, and automation tools to find and qualify potential investors for startups.

### Key Features
- **Multi-Agent AI Architecture** with 6 specialized agents
- **Real Deep-Search v3** with 4 AI provider integration (Claude, OpenAI, Gemini, Grok)
- **Automated Web Scraping** via Apify integration
- **Contact Enrichment** through Apollo.io API
- **Browser Automation** using Model Context Protocol (MCP)
- **Real-time Progress Tracking** and workflow management
- **Cost Control** with budget caps and usage monitoring
- **Deduplication Engine** with fuzzy matching algorithms

## 🏗️ System Architecture

### Core Components
1. **API Server** (`api_server.py`) - FastAPI-based backend serving 1519 lines
2. **Real Deep-Search Engine** (`real_deep_search_multi_provider.py`) - 6-stage AI pipeline
3. **Multi-Agent System** (LinkedIn Agent System) - Coordinated investor discovery
4. **Database Layer** - Supabase/PostgreSQL with RLS
5. **Frontend Integration** - Multiple UI implementations
6. **External Integrations** - Apify, Apollo, MCP browser automation

### Multi-Agent Architecture

```
Coordinator Agent
├── Scraper Agent (Apify integration)
├── Classifier Agent (Claude Haiku)
├── Searcher Agent (4 AI providers)
├── Enricher Agent (Apollo.io)
├── Scorer Agent (Custom scoring algorithm)
└── Browser Agent (MCP automation)
```

## 🚀 API Server Features

### Core Endpoints (`api_server.py:1-1519`)

#### Workflow Management
```python
POST /start_workflow
GET /workflow/{workflow_id}/status  
POST /workflow/{workflow_id}/stop
```

#### Expansion System
```python
POST /expansion/start
GET /expansion/{expansion_id}/status
GET /expansion/{expansion_id}/results
```

#### Progress Tracking
```python
GET /progress/{job_id}
WebSocket /ws/progress/{job_id}  # Real-time updates
```

#### Configuration Management
```python
GET /config/providers
POST /config/budget
GET /config/templates
```

## 🔍 Real Deep-Search v3 Multi-Provider

### 6-Stage Pipeline (`real_deep_search_multi_provider.py`)

1. **Scraping Stage** - Website content extraction (10KB summaries)
2. **Classification Stage** - Industry/stage/geography analysis
3. **Prompt Generation** - AI-generated search queries
4. **Multi-Provider Search** - Parallel queries across 4 AI providers
5. **Deduplication** - Advanced matching algorithms
6. **Scoring** - 5-component investor eligibility formula

### AI Provider Integration

```python
# Supported Providers
- Claude Sonnet 4: Primary reasoning and web search
- OpenAI GPT-4/o3: Scoring and analysis
- Gemini 2.5 Pro: Deduplication and classification  
- Grok 4: Alternative search provider
```

### Cost Management
- **Budget Caps**: Configurable per workflow
- **Token Tracking**: Real-time usage monitoring
- **Provider Optimization**: Cost-aware routing
- **Usage Analytics**: Detailed cost breakdowns

## 📊 Database Schema

### Core Tables (Supabase)

```sql
-- User Management
users (id, email, created_at, subscription_tier)

-- Job Management  
search_jobs (id, user_id, startup_url, status, created_at)
analysis_results (id, job_id, provider, response_data, score)

-- Smart-Money Radar v4 Tables
prompt_runs (id, job_id, provider, prompt_template, response, cost)
prompt_templates (id, provider, template_type, content, is_active)
investor_watchlist (id, investor_name, firm, linkedin_url, added_date)
liquidity_events (id, investor_id, event_type, description, detected_date)
```

### Performance Features
- **17 Indexes** for query optimization
- **Row Level Security** policies
- **Auto-updating timestamps** via triggers
- **Utility functions** for statistics and cleanup

## 🛠️ LinkedIn Agent System

### Tool Schema (`tools/schemas.json`)

#### Web Scraping Tools
```json
{
  "name": "apifyWebScrape",
  "description": "Sync scrape a startup homepage and return {html, text}",
  "maxDepth": 1,
  "maxCrawlPages": 1
}
```

#### AI Search Tools  
```json
{
  "name": "claudeDeepSearch", 
  "description": "Query Claude Sonnet 4 with web_search for investors",
  "maxTokens": 1024
}
```

#### Browser Automation
```json
{
  "name": "browserNavigate",
  "description": "Navigate to a URL using MCP browser and return page content",
  "wait_for": "body",
  "timeout": 30000
}
```

#### Contact Enrichment
```json
{
  "name": "apolloBatchEnrich",
  "description": "Enrich ≤300 investor names with emails",
  "maxItems": 300
}
```

### Searcher Agent (`agents/sub_agents/searcher.py`)

#### Parallel Search Implementation
```python
async def parallel_search(self, classification: Dict) -> Dict[str, Dict]:
    # Run searches across all available providers
    tasks = {
        "claude": self._search_claude(search_prompt),
        "gemini": self._search_gemini(search_prompt), 
        "grok": self._search_grok(search_prompt)
    }
    
    # Parallel execution with error handling
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
```

#### Advanced Deduplication
```python
def _deduplicate_investors(self, investors: List[Dict]) -> List[Dict]:
    # Name normalization and similarity matching
    # Consensus scoring across providers
    # Completeness bonus weighting
```

## 💰 Cost Structure & Optimization

### Per-Provider Pricing
- **Claude Sonnet**: $3/$15 per 1M tokens (input/output)
- **Gemini 2.5 Pro**: $1.25/$5 per 1M tokens
- **Grok 4**: ~$30/$60 per 1M tokens (estimated)
- **OpenAI GPT-4**: Variable by model

### Budget Controls
- Configurable caps per workflow
- Real-time usage tracking
- Provider cost optimization
- Automatic workflow stopping at limits

## 🔧 External Integrations

### Apify Web Scraping
- Startup homepage analysis
- 10KB content summaries
- Structured data extraction
- Rate limiting and error handling

### Apollo.io Contact Enrichment  
- Batch processing (≤300 names)
- Email discovery
- LinkedIn profile matching
- Contact verification

### Model Context Protocol (MCP)
- Browser automation
- LinkedIn navigation
- Crunchbase integration
- Profile verification

## 📱 Frontend Integration

### Progress Tracking UI
- Real-time WebSocket updates
- Stage-by-stage progress indicators  
- Cost tracking displays
- Error handling and retry mechanisms

### Configuration Interface
- Provider API key management
- Budget setting controls
- Template customization
- Workflow management

## 🚀 Deployment & Configuration

### Environment Variables
```bash
# AI Provider Keys
CLAUDE_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key  
GEMINI_API_KEY=your_gemini_key
GROK_API_KEY=your_grok_key

# External Services
APIFY_API_TOKEN=your_apify_token
APOLLO_API_KEY=your_apollo_key

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_key

# Server Configuration  
API_HOST=0.0.0.0
API_PORT=8000
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```
## 🧪 Testing & Quality Assurance

### Test Coverage
- Database connectivity tests
- API endpoint validation
- AI provider integration tests
- Cost calculation verification
- Deduplication algorithm testing

### Performance Monitoring
- Response time tracking
- Error rate monitoring  
- Cost per workflow analysis
- Success rate by provider

## 📈 Usage Analytics

### Key Metrics
- Workflows processed
- Investors discovered per job
- Average cost per investor
- Provider success rates
- Deduplication effectiveness

### Reporting Features
- Daily usage summaries
- Cost breakdowns by provider
- Performance trend analysis
- Error pattern identification

## 🔒 Security Features

### Data Protection
- Row Level Security (RLS) policies
- API key encryption
- Secure credential storage
- Input validation and sanitization

### Access Control
- User-based data isolation
- Role-based permissions
- Rate limiting
- Request logging

## 🎯 Smart-Money Radar v4 Features

### 5-Component Scoring Formula
1. **Industry Match** (0-100 points)
2. **Stage Preference** (0-100 points)  
3. **Geographic Proximity** (0-50 points)
4. **Portfolio Relevance** (0-100 points)
5. **Investment Activity** (0-50 points)

**Total Score**: 0-400 points with confidence ratings

### 14-Day Liquidity Monitoring
- NewsAPI integration for market events
- EDGAR filing tracking
- Automated investor alerts
- Portfolio company monitoring

### Template Management
- 12 default prompt templates (3 per provider)
- AI-generated custom templates
- A/B testing capabilities
- Performance-based optimization

## 🔄 Workflow Examples

### Complete Investor Discovery
```python
1. Submit startup URL → Scraping Stage
2. Extract 10KB summary → Classification Stage  
3. Generate AI prompts → Multi-Provider Search
4. Deduplicate results → Scoring Stage
5. Enrich with Apollo → Final Results
6. 14-day monitoring → Liquidity Alerts
```

### Budget-Controlled Expansion
```python
1. Set budget cap (e.g., $50)
2. Configure provider priorities
3. Real-time cost tracking
4. Automatic workflow stopping
5. Cost optimization recommendations
```

## 📋 API Documentation

### Workflow Endpoints

#### Start New Workflow
```http
POST /start_workflow
Content-Type: application/json

{
  "startup_url": "https://example.com",
  "budget_cap": 25.00,
  "providers": ["claude", "gemini", "grok"],
  "max_investors": 50
}
```

#### Get Workflow Status  
```http
GET /workflow/{workflow_id}/status

Response:
{
  "id": "wf_123",
  "status": "running",
  "stage": "searching", 
  "progress": 65,
  "cost_used": 12.50,
  "investors_found": 23,
  "estimated_completion": "2024-01-15T10:30:00Z"
}
```

### Real-time Progress WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/progress/wf_123');
ws.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(`Stage: ${progress.stage}, Progress: ${progress.progress}%`);
};
```

## 🎯 Advanced Features

### Fuzzy Deduplication Algorithm
```python
def fuzzy_match_investors(investor1, investor2):
    # Name similarity using Levenshtein distance
    # Firm matching with normalization
    # LinkedIn URL cross-reference
    # Confidence scoring (0-1.0)
```

### Dynamic Prompt Generation
```python
def generate_context_aware_prompts(startup_profile):
    # Industry-specific keywords
    # Stage-appropriate language  
    # Geographic targeting
    # Competitive landscape analysis
```

### Multi-Provider Consensus Scoring
```python
def calculate_consensus_score(provider_results):
    # Weight by provider reliability
    # Cross-reference duplicate mentions
    # Aggregate confidence scores
    # Apply completeness bonuses
```

## 🚀 Getting Started

### Quick Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Set up Supabase database using `SUPABASE_SETUP.md`
5. Run API server: `python api_server.py`
6. Start workflows via API or frontend

### Production Deployment
1. Configure Docker environment
2. Set up load balancing
3. Configure monitoring and logging
4. Implement backup strategies
5. Set up CI/CD pipeline

---

## 📞 Support & Maintenance

This comprehensive platform requires ongoing maintenance of:
- AI provider API integrations
- Database schema updates  
- Cost optimization algorithms
- Security patch management
- Performance monitoring

The system is designed to be highly scalable and can handle multiple concurrent workflows while maintaining cost efficiency and data accuracy.
