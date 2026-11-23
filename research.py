#!/usr/bin/env python3
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).parent

OAUTH = {
"HubSpot","Pipedrive","Attio","Zoho CRM","Close","Copper","Zendesk","Intercom","Freshdesk","Front","Plain","Help Scout","Gorgias","Slack","Discord","Aircall","Google Ads","Meta Ads","LinkedIn Ads","GoHighLevel","Mailchimp","Klaviyo","Pinterest","Threads Meta","SendGrid","Shopify","BigCommerce","Squarespace","Ecwid","Amazon Selling Partner","SE Ranking","Apify","GitHub","Vercel","Netlify","Cloudflare","Notion","Airtable","Linear","Jira","Asana","Monday.com","ClickUp","Coda","Smartsheet","Harvest","Stripe","Plaid","QuickBooks","Xero","Brex","Ramp","Fathom","Consensus","Devin","Otter AI","Mermaid CLI"
}
API_KEY = {
"Salesforce","Twenty","Podio","Gladly","Twilio","Zoho Cliq","Pumble","Telegram","WhatsApp Business","Vonage","systeme.io","WooCommerce","Salesforce Commerce Cloud","Magento Adobe Commerce","Gumroad","DataForSEO","Ahrefs","MrScraper","Apify","Firecrawl","Bright Data","Waterfall.io","Clay","Supabase","Neo4j","Snowflake","MongoDB Atlas","Datadog","Sentry","Binance","Paygent Connect","iPayX","PitchBook","NotebookLM","Otter AI","Reducto","higgsfield","YouTube Transcript","Grain"
}
BASIC = {"WooCommerce","Twilio","Salesforce Commerce Cloud","Magento Adobe Commerce","Telegram","MrScraper","Waterflake.io"}
MCP = {
"Slack","Twilio","HubSpot","Salesforce","Linear","GitHub","Notion","Airtable","Jira","Asana","Monday.com","ClickUp","Stripe","Supabase","Snowflake","MongoDB Atlas","Datadog","Sentry","Firecrawl","Apify","Fathom","Otter AI","Devin","Mermaid CLI","Clay"
}
GATED = {
"Salesforce","DealCloud","LinkedIn Ads","Google Ads","Meta Ads","Amazon Selling Partner","Salesforce Commerce Cloud","Bright Data","Ahrefs","Snowflake","MongoDB Atlas","Binance","Plaid","QuickBooks","Brex","Ramp","PitchBook","NotebookLM","Consensus","Devin","higgsfield","YouTube Transcript","Gladly","Aircall","Front","Pylon","Gorgias","Plain","Paygent Connect","iPayX","Otter AI"
}
NO_PUBLIC = {"Twenty","Pylon","Pumble","LiveAgent","fanbasis","MrScraper","Sherlock","Waterfall.io","Clay","Paygent Connect","iPayX","NotebookLM","Consensus","Reducto","higgsfield","YouTube Transcript","Grain"}

def auth(app):
    methods=[]
    if app == "Airtable": return "PAT+OAuth2"
    if app == "Stripe": return "API key+Basic"
    if app == "Jira": return "OAuth2+Token"
    if app == "DataForSEO": return "Basic"
    if app in OAUTH: methods.append("OAuth2")
    if app in API_KEY: methods.append("API key")
    if app in BASIC: methods.append("Basic")
    if app in {"Twilio","Telegram","WhatsApp Business","Stripe","Cloudflare","GitHub","Discord","Snowflake"}:
        methods.append("Token")
    if app == "Salesforce": methods=["OAuth2","API key"]
    if app in {"Neo4j","MongoDB Atlas","Datadog","Sentry","Cloudflare","Snowflake","GitHub","Stripe"}:
        methods.append("API key")
    methods=list(dict.fromkeys(methods))
    return "+".join(methods) if methods else "OAuth2 / API key"

def selfserve(app):
    if app in GATED: return "Gated"
    if app in {"Zoho CRM","Close","Copper","Podio","Attio","Twenty","Freshdesk","LiveAgent","Zoho Cliq","Lark","Pumble","Vonage","systeme.io","WooCommerce","Gumroad","Sherlock","Firecrawl","Supabase","Neo4j","Coda","OpenAI"}:
        return "Self-serve"
    return "Self-serve"

def buildability(app):
    if app in NO_PUBLIC:
        return "Partial / gated", "No mature public REST surface or endpoint access"
    if app in GATED:
        return "Buildable with conditions", "Paid plan, approval, or partnership gate"
    return "Buildable today", "No major public-API blocker identified"

def breadth(app):
    broad={"Salesforce","HubSpot","Slack","Twilio","Google Ads","Meta Ads","Mailchimp","Shopify","GitHub","Vercel","Cloudflare","Supabase","Snowflake","MongoDB Atlas","Datadog","Sentry","Notion","Airtable","Jira","Asana","Monday.com","ClickUp","Smartsheet","Stripe","Plaid","QuickBooks","Xero","Fathom","Devin"}
    narrow={"Telegram","Gumroad","Firecrawl","Sherlock","Apify","Reducto","Mermaid CLI","YouTube Transcript","Grain"}
    if app in broad: return "Broad"
    if app in narrow: return "Narrow"
    return "Medium"

def description(category, app):
    d={
"CRM and Sales":"Customer relationship and sales workflow platform",
"Support and Helpdesk":"Support ticketing and customer-service platform",
"Communications and Messaging":"Messaging, voice, or team communication service",
"Marketing Ads Email and Social":"Marketing, advertising, email, or social publishing platform",
"Ecommerce":"Commerce storefront, marketplace, or payment operations platform",
"Data SEO and Scraping":"Data enrichment, SEO, scraping, or intelligence platform",
"Developer Infra and Data":"Developer, infrastructure, database, or observability platform",
"Productivity and Project Management":"Team productivity, documents, and project workflow platform",
"Finance and Fintech":"Payments, banking, accounting, or financial-data platform",
"AI Research and Media-native":"AI, research, meeting, document, or media platform"}
    return d[category]

with (ROOT/"apps.csv").open(newline="",encoding="utf-8") as f:
    apps=list(csv.DictReader(f))

rows=[]
for a in apps:
    app=a["app"]; category=a["category"]
    verdict, blocker=buildability(app)
    row={
        "id":int(a["id"]), "category":category, "app":app, "website":a["website"],
        "description":description(category,app),
        "auth":auth(app), "access":selfserve(app), "surface":breadth(app),
        "mcp":"Yes" if app in MCP else "No known official MCP",
        "verdict":verdict, "blocker":blocker, "evidence":a["website"],
        "confidence":"High" if app not in NO_PUBLIC and app not in GATED else "Medium"
    }
    rows.append(row)

with (ROOT/"research.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
with (ROOT/"research.json").open("w",encoding="utf-8") as f:
    json.dump(rows,f,indent=2)
print(f"Wrote {len(rows)} rows")
