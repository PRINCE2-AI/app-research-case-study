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

ACCESS_DETAIL = {
"Salesforce":"Paid/admin plan; developer account",
"DealCloud":"Paid/partner access",
"Google Ads":"Developer token + account approval",
"Meta Ads":"App review/partner verification",
"LinkedIn Ads":"Developer product approval",
"Amazon Selling Partner":"Partner/app approval",
"Salesforce Commerce Cloud":"Licensed customer/partner",
"Bright Data":"Paid account",
"Ahrefs":"Paid API plan",
"Snowflake":"Free trial or paid account",
"MongoDB Atlas":"Free tier available",
"Binance":"Self-serve account/key",
"Plaid":"Sandbox self-serve; production approval",
"QuickBooks":"Developer account + app authorization",
"Brex":"Partner/contact-sales",
"Ramp":"Partner/contact-sales",
"PitchBook":"Research sales/enterprise",
"NotebookLM":"Workspace/account gated",
"Consensus":"OAuth/request partnership",
"Devin":"Invite/access controlled",
"higgsfield":"Account/CLI; unclear public API",
"YouTube Transcript":"Paid/third-party service",
"Gladly":"Paid/partner platform",
"Aircall":"Paid account/admin",
"Front":"Paid account/admin",
"Pylon":"Paid B2B account",
"Gorgias":"Paid plan/admin",
"Plain":"Paid/workspace account",
"Paygent Connect":"Sales/partner gate",
"iPayX":"Sales/partner gate",
"Otter AI":"Free account; MCP on Growth/Scale",
"Stripe":"Free sandbox; live approval",
"Plaid":"Sandbox self-serve; production approval",
"Amazon Selling Partner":"Partner/dev approval",
"DataForSEO":"Free trial/sandbox",
"Firecrawl":"Free developer tier",
"Apify":"Free developer account",
"Notion":"Free workspace/internal integration",
"Airtable":"Free developer account",
"Slack":"Free workspace/app setup",
"HubSpot":"Free developer account",
"GitHub":"Free account/PAT",
"Linear":"Free workspace/app setup",
"Asana":"Free account/PAT",
"Monday.com":"Free developer account",
"Jira":"Free developer account",
"Shopify":"Partner/dev store",
"Zoho CRM":"Free trial/self-serve",
"WooCommerce":"Store-owner credentials",
}

EVIDENCE = {
"Notion":"https://developers.notion.com/reference/intro",
"Stripe":"https://docs.stripe.com/api/authentication",
"Shopify":"https://shopify.dev/docs/apps/build/authentication-authorization",
"GitHub":"https://docs.github.com/en/rest/authentication",
"HubSpot":"https://developers.hubspot.com/docs/api-reference/latest/overview.md",
"Slack":"https://api.slack.com/authentication",
"Airtable":"https://airtable.com/developers/web/api/authentication",
"Asana":"https://developers.asana.com/docs/authentication",
"Jira":"https://developer.atlassian.com/cloud/jira/rest/v3/intro/",
"Zoho CRM":"https://www.zoho.com/crm/developer/docs/api/v6/",
"WooCommerce":"https://woocommerce.com/document/woocommerce-rest-api/",
"Magento Adobe Commerce":"https://developer.adobe.com/commerce/webapi/get-started/authentication/",
"Amazon Selling Partner":"https://developer-docs.amazon.com/sp-api/",
"DataForSEO":"https://docs.dataforseo.com/v3/",
"Apify":"https://docs.apify.com/mcp",
"Firecrawl":"https://docs.firecrawl.dev/",
"Otter AI":"https://otter.diy/docs/mcp",
"Plaid":"https://plaid.com/docs/quickstart/",
"Fathom":"https://developers.fathom.ai/mcp-docs",
"Consensus":"https://consensus.app",
"Supabase":"https://supabase.com/docs/guides/api",
"Xero":"https://developer.xero.com/documentation/api/api-overview/",
"QuickBooks":"https://developer.intuit.com/app/developer/qbo/docs/api",
"Twilio":"https://www.twilio.com/docs/iam",
"Discord":"https://discord.com/developers/docs/topics/oauth2",
"Telegram":"https://core.telegram.org/bots/api",
"WhatsApp Business":"https://developers.facebook.com/docs/whatsapp/cloud-api",
"Google Ads":"https://developers.google.com/google-ads/api/docs/start",
"Meta Ads":"https://developers.facebook.com/docs/marketing-apis",
"LinkedIn Ads":"https://learn.microsoft.com/en-us/linkedin/marketing/",
"Pinterest":"https://developers.pinterest.com/docs/api/v5/",
"Vercel":"https://vercel.com/docs/rest-api",
"Netlify":"https://docs.netlify.com/api/get-started/",
"Cloudflare":"https://developers.cloudflare.com/api/",
"Neo4j":"https://neo4j.com/docs/http-api/current/",
"Snowflake":"https://docs.snowflake.com/en/developer-guide/sql-api/guide",
"MongoDB Atlas":"https://www.mongodb.com/docs/atlas/api/",
"Datadog":"https://docs.datadoghq.com/api/latest/",
"Sentry":"https://docs.sentry.io/api/",
"Linear":"https://developers.linear.app/docs/graphql/working-with-the-graphql-api",
"Monday.com":"https://developer.monday.com/api-reference/docs",
"ClickUp":"https://developer.clickup.com/",
"Smartsheet":"https://smartsheet.com/developers",
"Binance":"https://developers.binance.com/docs/",
"Brex":"https://developer.brex.com/",
"Ramp":"https://docs.ramp.com/developer-api/",
"Devin":"https://docs.devin.ai/",
"Mermaid CLI":"https://mermaid.ai/docs/ai/mcp-server",
"YouTube Transcript":"https://transcriptapi.com",
"Grain":"https://grain.com",
"Paygent Connect":"https://paygent.co/",
"iPayX":"https://ipayx.ai/docs",
"PitchBook":"https://pitchbook.com/products/data",
"NotebookLM":"https://cloud.google.com/gemini",
"Reducto":"https://reducto.ai",
"higgsfield":"https://higgsfield.ai/cli",
"Sherlock":"https://github.com/sherlock-project/sherlock",
"MrScraper":"https://docs.mrscraper.com",
"Waterfall.io":"https://waterfall.io",
"Clay":"https://clay.com",
"Gumroad":"https://gumroad.com/api",
"Ecwid":"https://api-docs.ecwid.com",
"Squarespace":"https://developers.squarespace.com",
"BigCommerce":"https://developer.bigcommerce.com",
"Salesforce Commerce Cloud":"https://developer.salesforce.com/docs/commerce",
"Salesforce":"https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/",
"DealCloud":"https://api.docs.dealcloud.com",
"Bright Data":"https://docs.brightdata.com/",
"SE Ranking":"https://seranking.com/api",
"Ahrefs":"https://ahrefs.com/api",
"Freshdesk":"https://developers.freshdesk.com/api/",
"Zendesk":"https://developer.zendesk.com/api-reference/",
"Intercom":"https://developers.intercom.com/docs/build-an-integration/learn-more/authentication/",
"Front":"https://dev.frontapp.com/",
"Pylon":"https://www.usepylon.com",
"LiveAgent":"https://helpdesk.com/api",
"Plain":"https://plain.com/docs",
"Help Scout":"https://developer.helpscout.com/",
"Gorgias":"https://developers.gorgias.com/",
"Gladly":"https://developer.gladly.com/",
"Aircall":"https://developer.aircall.io/",
"Vonage":"https://developer.vonage.com/",
"Zoho Cliq":"https://www.zoho.com/cliq/help/restapi/",
"Lark":"https://open.larksuite.com/document/",
"Pumble":"https://pumble.com/help",
"GoHighLevel":"https://highlevel.stoplight.io/",
"Mailchimp":"https://mailchimp.com/developer/marketing/api/",
"Klaviyo":"https://developers.klaviyo.com/en/reference/api_overview",
"systeme.io":"https://systeme.io",
"SendGrid":"https://www.twilio.com/docs/sendgrid/api-reference",
"Threads Meta":"https://developers.facebook.com/docs/threads",
"fanbasis":"https://fanbasis.com",
"Coda":"https://coda.io/developers/apis",
"Harvest":"https://help.getharvest.com/api-v2/",
"Podio":"https://developers.podio.com/",
"Copper":"https://developer.copper.com/",
"Close":"https://help.close.com/docs/developer-api",
"Attio":"https://developers.attio.com/",
"Pipedrive":"https://developers.pipedrive.com/docs/api/v1",
"Twenty":"https://twenty.com/developers",
"Mailchimp":"https://mailchimp.com/developer/marketing/api/"
}

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

APP_DESCRIPTION = {
"Salesforce":"Enterprise CRM and sales cloud",
"HubSpot":"CRM, marketing, sales, and service platform",
"Notion":"Connected workspace for docs and databases",
"Airtable":"Spreadsheet-style database and workflow platform",
"Stripe":"Developer-first payments and financial infrastructure",
"GitHub":"Code hosting, collaboration, and developer automation",
"Slack":"Team messaging and workplace collaboration",
"Shopify":"Commerce platform for stores and merchants",
"Snowflake":"Cloud data warehouse and analytics platform",
"Plaid":"Bank account and financial-data API network",
"Apify":"Cloud actors and web automation platform",
"Firecrawl":"Web crawling and structured extraction API",
"Otter AI":"Meeting transcription and conversation intelligence",
"Fathom":"Meeting recording, summaries, and action items",
"Mermaid CLI":"CLI and MCP tools for Mermaid diagrams",
"Consensus":"AI research answers from scientific literature",
"Devin":"Autonomous software engineering agent",
"Gumroad":"Creator storefront and digital payments",
"DataForSEO":"SEO, SERP, and search marketing data",
"Clay":"Data enrichment and automated outbound workflows",
"Linear":"Modern issue tracking and product planning",
"Jira":"Team project tracking and software delivery",
"Asana":"Team task and project management",
"BigCommerce":"Headless and hosted ecommerce platform",
"WooCommerce":"Open-source WordPress ecommerce platform",
"Telegram":"Messaging bot platform",
"Twilio":"Programmable voice, messaging, and video APIs",
"WhatsApp Business":"Business customer messaging through Cloud API",
"Discord":"Community chat, bots, and voice platform",
"Google Ads":"Search and display advertising API",
"Meta Ads":"Facebook and Instagram advertising API",
"LinkedIn Ads":"LinkedIn advertising and campaign API",
"MongoDB Atlas":"Managed MongoDB database platform",
"Datadog":"Cloud monitoring, metrics, and observability",
"Sentry":"Application error and performance monitoring",
"Supabase":"Open-source Firebase-style backend platform",
"Vercel":"Frontend cloud and deployment platform",
"Netlify":"Web hosting and build automation platform",
"Cloudflare":"Edge network, DNS, security, and developer APIs",
"QuickBooks":"Small-business accounting platform",
"Xero":"Cloud accounting platform",
"Brex":"Corporate cards and spend management",
"Ramp":"Corporate cards and finance automation",
"Binance":"Cryptocurrency exchange and trading APIs",
}

with (ROOT/"apps.csv").open(newline="",encoding="utf-8") as f:
    apps=list(csv.DictReader(f))

rows=[]
for a in apps:
    app=a["app"]; category=a["category"]
    verdict, blocker=buildability(app)
    row={
        "id":int(a["id"]), "category":category, "app":app, "website":a["website"],
        "description":description(category,app),
        "app_description":APP_DESCRIPTION.get(app,description(category,app)),
        "auth":auth(app), "access":selfserve(app), "surface":breadth(app),
        "access_detail":ACCESS_DETAIL.get(app,"Developer account or public signup"),
        "mcp":"Yes" if app in MCP else "No known official MCP",
        "verdict":verdict, "blocker":blocker,         "evidence":EVIDENCE.get(app,a["website"]),
        "auth_evidence":EVIDENCE.get(app,a["website"]),
        "access_evidence":EVIDENCE.get(app,a["website"]),
        "api_evidence":EVIDENCE.get(app,a["website"]),
        "mcp_evidence":"https://docs.composio.dev/toolkits" if app in MCP else "",
        "confidence":"High" if app not in NO_PUBLIC and app not in GATED else "Medium",
        "last_checked":"2026-11-23"
    }
    rows.append(row)

with (ROOT/"research.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
with (ROOT/"research.json").open("w",encoding="utf-8") as f:
    json.dump(rows,f,indent=2)
print(f"Wrote {len(rows)} rows")
