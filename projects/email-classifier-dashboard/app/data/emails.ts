// Mock dataset based on 15,052 classified emails across 30 categories

export interface Email {
  id: string;
  date: string;
  subject: string;
  from: string;
  category: string;
  confidence: number;
}

export interface CategoryCount {
  category: string;
  count: number;
  percentage: number;
}

const CATEGORIES = [
  "AI/ML", "Finance", "Shopping", "Travel", "Health", "Legal", "Education",
  "Social", "News", "Promotions", "Updates", "Security", "Work", "Personal",
  "Receipts", "Subscriptions", "Government", "Insurance", "Banking", "Utilities",
  "Real Estate", "Automotive", "Food", "Entertainment", "Sports", "Technology",
  "Communication", "Career", "Family", "Other"
] as const;

// Realistic distribution - some categories are much more common
const CATEGORY_COUNTS: Record<string, number> = {
  "Promotions": 2847,
  "Updates": 1956,
  "Shopping": 1423,
  "Finance": 1102,
  "Work": 987,
  "Technology": 876,
  "News": 823,
  "Social": 756,
  "Subscriptions": 634,
  "Communication": 521,
  "AI/ML": 487,
  "Receipts": 445,
  "Personal": 398,
  "Banking": 367,
  "Security": 312,
  "Entertainment": 289,
  "Education": 267,
  "Career": 234,
  "Travel": 212,
  "Health": 198,
  "Food": 176,
  "Legal": 145,
  "Insurance": 134,
  "Utilities": 123,
  "Government": 112,
  "Family": 98,
  "Sports": 87,
  "Automotive": 76,
  "Real Estate": 65,
  "Other": 53,
};

export const TOTAL_EMAILS = 15052;

export function getCategoryBreakdown(): CategoryCount[] {
  return CATEGORIES.map(cat => ({
    category: cat,
    count: CATEGORY_COUNTS[cat] || 0,
    percentage: ((CATEGORY_COUNTS[cat] || 0) / TOTAL_EMAILS) * 100,
  })).sort((a, b) => b.count - a.count);
}

// Sample subjects for each category
const SUBJECT_SAMPLES: Record<string, string[]> = {
  "AI/ML": ["New GPT-5 API access granted", "Your ML model training complete", "AI Weekly Digest #234", "Hugging Face: New model available", "OpenAI API usage report"],
  "Finance": ["Your monthly statement is ready", "Investment portfolio update", "Tax document available", "Dividend payment received", "Market alert: Portfolio change"],
  "Shopping": ["Your order has shipped!", "Order confirmation #38291", "Your package is out for delivery", "Price drop alert on your wishlist", "Your Amazon order arrives today"],
  "Travel": ["Flight confirmation: LHR to NRT", "Hotel booking confirmed", "Your trip itinerary", "Booking.com: Special offer", "Rail ticket confirmation"],
  "Health": ["Appointment reminder: Dr. Smith", "Your prescription is ready", "Lab results available", "Health insurance claim update", "Wellness report ready"],
  "Legal": ["Contract ready for review", "Terms of service update", "Privacy policy changes", "Legal document signed", "NDA execution confirmed"],
  "Education": ["Course enrollment confirmed", "New lesson available", "Certificate of completion", "Coursera: New course recommendation", "Assignment feedback ready"],
  "Social": ["You have 5 new followers", "Someone mentioned you", "New connection request", "Event invitation", "Friend request from John"],
  "News": ["Breaking: Tech industry update", "Morning Brew Daily Digest", "The Information: Daily Brief", "Reuters: Market recap", "Hacker News Daily Top 10"],
  "Promotions": ["50% off everything today!", "Flash sale starts now", "Exclusive member offer", "Last chance: Deal expires tonight", "New arrival: Just for you"],
  "Updates": ["App update available", "Your account has been updated", "System maintenance scheduled", "Feature announcement", "Service status update"],
  "Security": ["New login from Chrome on Mac", "Two-factor authentication enabled", "Password changed successfully", "Suspicious activity detected", "Security review recommended"],
  "Work": ["Meeting notes: Q1 Planning", "Slack: New message in #general", "Jira ticket assigned to you", "PR review requested", "Sprint retrospective summary"],
  "Personal": ["Happy Birthday!", "Photos shared with you", "Reminder: Mom's anniversary", "Family dinner this Saturday", "Your memories from 3 years ago"],
  "Receipts": ["Receipt for your payment", "Invoice #INV-2026-0342", "Payment confirmation", "Transaction receipt", "Your receipt from Apple"],
  "Subscriptions": ["Your subscription renewed", "Billing statement", "Membership renewal notice", "Plan upgrade confirmation", "Subscription expiring soon"],
  "Government": ["HMRC: Tax return received", "Council tax notification", "Government gateway update", "Passport application update", "Electoral roll confirmation"],
  "Insurance": ["Policy renewal reminder", "Claim status update", "Insurance quote ready", "Coverage summary", "Annual policy review"],
  "Banking": ["Direct debit confirmation", "Account balance alert", "New payee added", "Standing order updated", "Savings goal reached"],
  "Utilities": ["Your energy bill is ready", "Water bill statement", "Broadband usage summary", "Council tax payment due", "Gas meter reading reminder"],
  "Real Estate": ["Property alert: New listing", "Mortgage statement", "Rental agreement update", "Property valuation ready", "Lease renewal notice"],
  "Automotive": ["MOT reminder", "Service booking confirmed", "Car insurance renewal", "Fuel receipt", "Vehicle tax due"],
  "Food": ["Your Deliveroo order is confirmed", "Tesco: Your groceries are ready", "Restaurant reservation confirmed", "Recipe of the week", "Meal plan ready"],
  "Entertainment": ["Netflix: New releases this week", "Your Spotify Wrapped", "Concert tickets confirmed", "Steam: Wishlist item on sale", "Disney+: New episode available"],
  "Sports": ["Match highlights available", "Fantasy league update", "Gym membership renewed", "Race registration confirmed", "Fitness goal achieved"],
  "Technology": ["GitHub: New release available", "npm: Package update", "Your cloud usage report", "Developer newsletter", "API deprecation notice"],
  "Communication": ["Voicemail from +44 7700", "Missed call notification", "WhatsApp backup complete", "Telegram: New message", "Signal: Group invite"],
  "Career": ["New job match found", "Application received", "Interview scheduled", "LinkedIn: Profile views", "Salary survey results"],
  "Family": ["Shared album updated", "Family calendar event", "School newsletter", "Parent-teacher evening", "Family reunion planning"],
  "Other": ["Miscellaneous notification", "Uncategorized alert", "System notification", "General update", "Automated message"],
};

const SENDERS: Record<string, string[]> = {
  "AI/ML": ["noreply@openai.com", "team@huggingface.co", "newsletter@deeplearning.ai"],
  "Finance": ["statements@bank.co.uk", "alerts@trading212.com", "noreply@wise.com"],
  "Shopping": ["ship-confirm@amazon.co.uk", "orders@apple.com", "noreply@ebay.co.uk"],
  "Travel": ["bookings@ba.com", "confirm@booking.com", "tickets@trainline.com"],
  "Promotions": ["deals@retailer.com", "offers@brand.com", "marketing@store.com"],
  "Updates": ["noreply@github.com", "updates@app.com", "system@service.com"],
  "Security": ["security@google.com", "noreply@auth0.com", "alerts@1password.com"],
  "Work": ["notifications@slack.com", "jira@company.com", "noreply@linear.app"],
  "Technology": ["noreply@github.com", "npm@npmjs.com", "cloud@google.com"],
  "News": ["digest@morningbrew.com", "daily@theinformation.com", "news@reuters.com"],
};

function randomDate(daysBack: number): string {
  const d = new Date();
  d.setDate(d.getDate() - Math.floor(Math.random() * daysBack));
  d.setHours(Math.floor(Math.random() * 24), Math.floor(Math.random() * 60));
  return d.toISOString();
}

function generateMockEmails(count: number): Email[] {
  const emails: Email[] = [];
  const categories = getCategoryBreakdown();
  
  for (let i = 0; i < count; i++) {
    // Pick category weighted by distribution
    const cat = categories[i % categories.length].category;
    const subjects = SUBJECT_SAMPLES[cat] || SUBJECT_SAMPLES["Other"]!;
    const senders = SENDERS[cat] || [`noreply@${cat.toLowerCase().replace(/[/ ]/g, '')}.com`];
    
    emails.push({
      id: `email-${String(i).padStart(5, '0')}`,
      date: randomDate(90),
      subject: subjects[Math.floor(Math.random() * subjects.length)]!,
      from: senders[Math.floor(Math.random() * senders.length)]!,
      category: cat,
      confidence: 0.7 + Math.random() * 0.29,
    });
  }

  return emails.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

// Generate 200 sample emails for the recent table
export const recentEmails = generateMockEmails(200);
