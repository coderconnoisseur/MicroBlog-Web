# Rate Limiting Implementation

## Overview
Flask-Limiter has been integrated into the Microblog application to prevent abuse and ensure fair usage of the service.

## Configuration
Rate limiting is configured in `config.py`:
- **Default Limits**: 1000 requests per day, 100 per hour
- **Storage**: Memory-based (can be upgraded to Redis for production)
- **Headers Enabled**: Rate limit information is included in HTTP response headers

## Route-Specific Limits

### Authentication Routes
- **Login** (`/login`): 5 attempts per minute
  - Prevents brute force attacks
- **Registration** (`/register`): 3 attempts per minute
  - Prevents spam account creation
- **Password Reset Request** (`/reset_password_request`): 2 per minute
  - Prevents email flooding
- **Password Reset** (`/reset_password/<token>`): 3 per minute
  - Prevents token abuse

### User Actions
- **Post Creation** (`/index` POST): 10 posts per minute
  - Prevents spam posting
- **Follow/Unfollow** (`/follow/<username>`, `/unfollow/<username>`): 20 actions per minute
  - Prevents automated following/unfollowing

### API Routes
- **Rate Limit Status** (`/api/rate-limit-status`): 30 requests per minute
  - For monitoring purposes

## Error Handling
When rate limits are exceeded:
- **HTTP Status**: 429 (Too Many Requests)
- **Custom Template**: `429.html` with user-friendly error message
- **Auto-Refresh**: Page automatically refreshes after the retry period
- **API Response**: JSON format for API endpoints

## Response Headers
Rate limit information is included in response headers:
- `X-RateLimit-Limit`: The rate limit ceiling for the given endpoint
- `X-RateLimit-Remaining`: The number of requests left for the current time window
- `X-RateLimit-Reset`: The time when the current rate limit window resets

## Testing Rate Limits
To test rate limits in development:
1. Try logging in with wrong credentials more than 5 times within a minute
2. Try creating multiple posts rapidly
3. Visit `/api/rate-limit-status` to check if rate limiting is active

## Production Considerations
For production deployment:
1. **Redis Storage**: Update `RATELIMIT_STORAGE_URL` to use Redis instead of memory
2. **Adjust Limits**: Modify limits based on expected usage patterns
3. **IP Whitelist**: Consider whitelisting trusted IPs if needed
4. **Monitoring**: Monitor rate limit violations for security insights

## Environment Variables
```bash
# Optional: Use Redis for rate limit storage in production
REDIS_URL=redis://localhost:6379/0
```

## Benefits
- **Security**: Prevents brute force attacks and automated abuse
- **Performance**: Protects server resources from excessive requests
- **Fair Usage**: Ensures all users get fair access to the service
- **User Experience**: Graceful error handling with informative messages