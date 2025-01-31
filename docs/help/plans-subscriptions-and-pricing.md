---
description: Use Warp for free or subscribe to a paid plan
---

# Plans, Subscriptions & Pricing

You can visit [warp.dev/pricing ](https://www.warp.dev/pricing)to learn about Warp's current plans and what's included in each offering.

This article includes answers to some frequent questions that might come up as you subscribe, manage billing, or pay invoices.

Don't have Warp yet? [Download now](../getting-started/getting-started-with-warp.md) and get started today.

## Warp’s Refund Policy

If you believe you've made a mistake signing up for a paid Warp subscription, please contact us at [billing@warp.dev](mailto:billing@warp.dev). We'll be happy to refund you the full amount if you downgrade your subscription within 72 hours of signing up for monthly billing, or within 30 days of signing up for annual billing.

We also may choose to offer refunds, on a case-by-case basis, if a severe product defect or problem with uptime availability occurs. As Warp is currently in public beta, there is no guaranteed uptime SLA. You may reference known issues as monitored on [Warp’s public GitHub issues page](https://github.com/warpdotdev/Warp/issues) and watch uptime on [Warp’s Status Page](https://status.warp.dev/). To request a refund, please email [billing@warp.dev](mailto:billing@warp.dev) with detailed information about your situation.

## Frequently asked questions

### How can I subscribe to a Pro or Team plan?

To subscribe to a paid Warp plan like Pro or Team, you must first [create a Team in Warp](../features/teams.md#creating-a-team). Then, you can [upgrade online](https://app.warp.dev/upgrade) or through the downloaded app. In the app, navigate to Settings → Teams and find the upgrade link. After you enter your payment information, you will receive an invoice and confirmation email from Warp.

### How can I subscribe to a Warp Enterprise plan?

Warp offers an Enterprise plan with custom pricing for larger engineering organizations or businesses with advanced security and compliance requirements. If you are interested in learning whether an Enterprise plan might be the best fit for your team, please [contact us](https://www.warp.dev/contact-sales) to kick off a conversation.

### How can I upgrade for more Warp AI requests, command suggestions, and tokens?

Both Warp’s Pro and Team plans include higher limits for Warp AI requests, command suggestions, and tokens than what’s currently available on the Warp Free plan. Even if you are working alone and not ready to invite additional team members for collaboration, you will need to [create a Team](../features/teams.md#creating-a-team) in Warp to upgrade to the paid Warp plan, which unlocks access to higher AI limits.

If you are not planning on extending invites to any team member collaborators, we suggest creating a Team with your name, e.g. “Zach’s Team” or “My Personal Team.” Then you can [upgrade online](https://app.warp.dev/upgrade) or in the downloaded app by navigating to Settings → Teams and finding the upgrade link.

### What counts as a team member and how does billing work for members?

In Warp, a team member is a seat with access to your Team, which includes access to the shared team Warp Drive and any shared objects like Notebooks or Workflows in that Warp Drive. Every Warp Drive team on any plan allows an unlimited number of users. However, to gain access to more features and higher limits, you will need to upgrade to a tier that includes those features. Upgrading a Warp Drive team to a new tier upgrades both your account as well as the accounts of all members on the same team.\
\
Warp's Free plan includes access to share up to a limited number of Notebooks and Workflows with a team of other Free members. Beyond the limit, you will be prompted to [upgrade to a Warp Team plan](https://app.warp.dev/upgrade) to share more.\
\
After upgrading to a Pro or Team plan, you will be notified by email as additional team members accept invites to join the team. Each team member is billed at the rate of $25 per member per month if you’re paying month-to-month or $22 per member per month if you are committing annually. Billing for the team member applies to every day the team member has access to your team.

There are differences in how members are billed based on your payment schedule:

* **Monthly Plan:** New members' prorated usage is added to the next invoice.
* **Annual Plan:** New members' prorated usage is invoiced immediately.

Billing is prorated, meaning you only pay for the time the member is part of your team during the billing period. For example, if a member joins your team's monthly plan halfway through the month, you will be charged just half of the monthly fee ($12.50 out of $25). Similarly, if a member joins with four months remaining in an annual plan, you will be charged for those four months only, which amounts to $88 (4/12 of the annual $264).

If a member leaves part way through the billing cycle, Warp will issue a prorated credit based on the unused portion of their membership. This credit is applied to your team's next invoice, regardless of whether you're on a monthly or annual plan.

### My co-workers are using Warp but we’re not on a Team together yet. How does billing work?

Individual users with either personal or work email domains may continue to use Warp independently without incurring billing. The benefit of joining together on a Warp Team is that you get access to a shared Team Drive and collaboration features.

When you’re ready to use Warp more collaboratively, we suggest you nominate an Admin to [create a Team](https://docs.warp.dev/features/teams) and invite members to join. When your Team exceeds the Warp Drive limits, you will be prompted to upgrade to a Team plan.

### What happens when I downgrade during a billing cycle?

When you upgrade to a Warp Team plan, you can subscribe monthly or annually.

You can initiate a downgrade at any point throughout your subscription through the billing portal by going to `Settings > Teams > Manage billing`. The subscription will be canceled at the end of your billing cycle, monthly or yearly.

You can continue to use your Warp Team plan features until the cycle end date. Any additional team members added to your team will be invoiced at the end of your billing cycle.

### What happens if I upgrade from monthly to annual billing?

When upgrading from a monthly to annual billing cycle the billing is prorated, meaning you only pay for the annual portion of the year you haven't paid for yet. You will be billed for the remaining part of the billing year with the discounted rate.\
\
You can initiate a upgrade at any point throughout your subscription through the billing portal by going to `Settings > Teams > Manage billing`.

### What happens if my payment fails?

If a payment fails, you will receive an email from Stripe and your Warp Team Settings will show a past-due alert. Certain Team plan features and the ability to invite new members will be locked down while your Team is in a past-due state. Paying the most recent invoice through the [billing portal](https://app.warp.dev/upgrade) will fully re-enable your Team plan features.

### What counts as a Warp AI request or command suggestion?

[Warp AI](../features/warp-ai/) includes [Agent Mode](../features/warp-ai/agent-mode.md), [Active AI](../features/warp-ai/active-ai.md), [Generate](../features/warp-ai/generate.md), and [AI Autofill](../features/warp-drive/workflows.md#ai-autofill) in Warp Drive.

Every time you submit an AI query with Agent Mode, it counts as one AI request. Agent Mode suggested commands and requested commands do not count as AI requests.

Active AI features like Next Command have a seperate counter and only count when accepted.\
\
[Generate](../features/warp-ai/generate.md) lets you look up commands or contextual suggestions as you’re typing. As you’re entering and adjusting a query to look up a command suggestion, you may incur multiple AI requests before selecting a suggestion.\
\
Anytime you run AI Autofill in Warp Drive, this counts as one AI request.

Request limits are allocated at the seat level to Warp users or team members. You can follow along with your request limits by referencing the counter under `Settings > AI`.

### What counts as a Warp AI token?

Tokens are chunks of text, such as words, parts of code, or characters, that large language models (LLMs) break down to analyze and generate responses. LLMs have a maximum number of tokens they can process at once. Warp AI Requests and Suggestions are not the same as Tokens, which are limited separately regardless of which plan you're on. \
\
Please learn more about Tokens [here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them) and refer to [pricing](https://www.warp.dev/pricing) for the current monthly token limits on each plan.

### How often does my Warp AI request, token, and suggestion limits reset?

Allotted AI requests and command suggestions limits reset every 30 days from your signup date. When you upgrade to a Pro or Team plan, you will be given a higher request limit immediately. You can follow along with your refill period by referencing the counter under Settings -> AI.

### How can I get the most out of my Warp Team plan?

The main benefits of a Warp Team plan are related to team collaboration and knowledge sharing, async, and in real-time. You can make the most of your Team plan by creating an organized Warp Drive with [Notebooks](../features/warp-drive/notebooks.md) and [Workflows](../features/warp-drive/workflows.md) to help your team streamline processes. Be sure to try out [Session Sharing](https://docs.warp.dev/features/session-sharing) for pair programming!

### Can I use a Free plan if I'm a developer at a large company or organization?

Yes, absolutely. If you're using Warp at work, you may benefit from upgrading to a Team plan or an Enterprise plan for collaboration or plan features. However, Warp does not force companies of a certain size to upgrade to a paid plan. You are welcome to take advantage of Warp's Free plan.

### Are there any Warp discounts for students, non-profits, or open-source teams?

At this time, Warp does not offer any discounts for students, non-profits, or open-source teams. We recommend checking out Warp’s Free plan which includes all of the core terminal features.

### Where is Warp Drive data for my team stored?

Warp Drive data is stored securely on Google Cloud Platform servers in the United States. Data is encrypted in transit and at rest. Please [visit the Security Overview](https://www.warp.dev/security) for more information and contact [security@warp.dev](mailto:security@warp.dev) if you need further details.

### What does “Free preview” mean in Warp?

Before the launch of the Warp Team plan, certain features like Warp Drive for Teams and Warp AI were available in a Free Preview. This allowed early adopters of Warp to experiment with these features while they were in development. The Free Preview for Warp AI and Warp Drive for Teams has ended. Additional features may be listed in Free Preview in the future.

### What does “Early adopter” mean in Warp?

During the Free Preview period of Warp Drive for Teams, several customers went above and beyond to provide ongoing design feedback and partnership with the Warp Product Team. If your Team was part of this program, you may see a special “Early adopter” label on the Team settings in your account. Early adopter teams have some custom pricing and plan exemptions in place. Please contact your Warp Team Admin for more information about how this status affects your account.

### What payment options are available for Warp's self-service plans?

Warp uses Stripe for payment processing; the only available payment method is by credit card.

Warp cannot currently accept payment by ACH, cash, check, money order, or cryptocurrency.

### How do I cancel my subscription?

You can cancel at any point throughout your subscription through the billing portal by going to `Settings > Teams > Manage billing`. Cancelled subscriptions will remain active until the end of the billing cycle.

### How do I get a refund?

For monthly subscriptions, we in general do not issue refunds. You can remove the users you do not want to pay for in `Settings > Teams > Team Members`. You will only be refunded in credits for Warp on a prorated basis.

### Why can't I subscribe to Warp?

There are certain prohibited and restricted businesses in which Stripe and major credit card networks will not process payments. For the most updated information, please see the full list [here](https://stripe.com/legal/restricted-businesses).

### I have a question and need help. How can I reach a human at Warp?

The team at Warp is standing by and ready to help you with any questions you have about your plan or subscription. Please email us at [billing@warp.dev](mailto:billing@warp.dev) and we will get back to you.

\
Don't have Warp yet? [Download now](../getting-started/getting-started-with-warp.md) and get started today.
