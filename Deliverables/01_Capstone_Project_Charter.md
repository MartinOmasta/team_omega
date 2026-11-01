---
output:
  html_document: default
  pdf_document: default
  word_document: default
---

# Capstone Project Charter

The purpose of this charter is to establish a shared understanding of your team's project before you begin. It should identify the problem you are addressing, why it matters, who might benefit from the results, and what data you will use.

__This is not a research proposal or a full analysis plan.__ You will develop your project background/rationale and full analysis plan during Sprint 2 of the Capstone.

Keep your responses concise. Aim for approximately 1–2 pages.

## Project Information

__Project title:__ Norwegian Heating - It's Electric! (This just popped in my brain, can totally change it if you don't like it -BCN)

__Team name:__ Team-Omega.

__Team members:__ Anthony Ruoti, Benjamin Niemi, Martin Omasta

__Project source:__

- [x] Capstone Curated Project Bank

- [ ] Alternative project approved by instructor

### Problem and Context

__What problem are you trying to address?__

Describe the problem in a few sentences. What is happening that an organization, business, agency, or community would want to understand, predict, or improve?

*Example:* A subscription-based company is experiencing customer attrition. When customers cancel their subscriptions, the company loses recurring revenue and may incur additional costs to acquire replacement customers.

__Your response: Which households shift electricity use in response to variable pricing, and can we predict their flexibility?
We decided to use the prompt question as our base, and contextually flesh out the results with the additional questions listed below. 

### Why Does This Problem Matter?

Briefly explain why the problem is important in its organizational, business, healthcare, public sector, or other applied context. You do not need to provide a literature review or fully support your rationale with sources yet; you will develop the background and rationale during Sprint 2.

__Consider__:
- What consequences might result from this problem?
- Why might an organization or stakeholder want to address it?
- What decisions could a better understanding of the problem inform?

*Example:* Understanding customer attrition could help a company evaluate its retention strategies and determine where to focus customer support or engagement resources.

__Your response: The problem presented above are related to heating during Norwegian winters, the cost of heating and the reliance on electricity are of utmost importance for the health and wellbeing of specifically the Norwegian residents, though possibly applicable to colder climate countries at large. As many nations begin pivoting from carbon heavy fossil fuels to more renewable energy source it is important to investigate the topic of the cost of energy itself, and as this is in one of the more inhospitable climates during the winter this data can share important insights. If the power is unreliable or too expensive then the populace at large could be harmed during this pivot, energy suppliers will need to take this into account when they move energy prices and influence policies. 

### Stakeholder and Intended Use

__Who would care about the results of this project?__

Identify the primary stakeholder or intended audience. This could be a business unit, organizational decision-maker, public agency, healthcare provider, or other group.

BCN: I think that the three main target audiences would be Governments, Electrical companies and the population at large. 

__Primary stakeholder:__

__What might this stakeholder want to learn or do with the results?__

*Example:* A customer retention team might use the results to better understand which customer characteristics or behaviors are associated with cancellation and to inform future retention strategies.

__Your response: 
                  Government: The effects that policy will make on the constituents and how best to guide that forward keeping in mind the health and well-being of the populace. 
                  Electric companies: How to maintain a customer base and keep houses heated, maintain affordability and profitability.
                  Populace: Gain information to use for more informed business, and political decisions. 

Ipsos and other power companies who want to maximize profit by increasing price without losing demand. Those who can maximize profit prior to dimishing returns.

### Data Overview

__What data will you use to investigate the problem?__

Identify the dataset and briefly describe what it contains. For a project from the Capstone curated project bank, use the information provided in the project description. Remember, you have the option to refine the project goal or question while still using the same data source!

| Item | Description |
|---|---|
| Dataset name | A rich dataset of hourly residential electricity consumption data and survey answers from the iFlex dynamic pricing experiment. |
| Data source | https://doi.org/10.5281/zenodo.8248802 |
| Unit of analysis (e.g., customer, transaction, patient) | Electricity usage in kWH during Norwegian Winters |
| Approximate number of observations, if known |  13.52 Million. |
| General types of information available | Participant ID, Date, Hour of the day, Participation in phase, kWH Demand, Price Signal, Temperature recordings |
| Data access confirmed? | Yes |

__How might these data help address the problem?__

Briefly explain what information in the dataset could be relevant to the problem.

*Example:* The dataset contains customer demographics, subscription information, service usage, and cancellation status. These data may help the team examine patterns associated with customer attrition.

__Your response: As this is real world recorded data from a study with the citizens of Norway participating it lends itself to a high level of interest. Norway is a high latitude country which experiences harsh winters with extremely low temperatures. Heating is a crucial issue for those individuals living there and with the prevalence of electric heaters it's very useful to have a data set that measures the usage, along with a variety of pricing experiments and surveys to understand the thoughts of the citizens. 

[Describe the relevance of the data to the problem.]

### The Data Science Opportunity

__What could data science / machine learning / AI practices help you accomplish here?__

At a high level, describe what you hope to learn or accomplish using the available data. You do not need to specify particular algorithms, preprocessing steps, or evaluation metrics here; those belong in the Analysis Plan due in Sprint 2.

*Example:* The team could use historical customer information to identify patterns associated with churn and investigate whether customer cancellation can be predicted using available customer characteristics and behaviors.

__Your response: Ideally using this dataset finding out how price experiments changed the electrical habits of the participants. (I was having a hard time with this one so, we can flesh it out later I think. -BCN

[Describe the intended analytical task in a few sentences.]

### Initial Questions and Unknowns

What do you still need to understand about the problem, the data, or the intended use of the results before beginning the analysis?

List up to three questions that your team expects to investigate during the background/rationale development and initial data exploration, both of which you will do during Sprint 2.

1. What effect does temperature have on kWh use of electrical consumption? 

2. What effect does time of day have on kwH use of electrical consumption?

3. Does the local area or the household size have an effect on kwH use of electrical consumption?

These are starting questions, not necessarily your final analytical question(s). You will refine your understanding of the problem and develop your Analysis Plan during Sprint 2.

### Project Risks

Project risks are uncertainties that can undermine a project's success. Sometimes we have ways to better control for or assess risks, and sometimes we do not. Your job is to try to identify at least 2 more risks to this project. I am starting you off with a risk everyone will always have at this stage in a project.

1. __The dataset chosen may not be suitable to address the problem/question exactly as posed.__

2. There may be gaps in the data, or not as comprehensive as would be helpful

3. Data includes survey answers with open ended questions, the subjectivity of them is difficult to quantitate or use in an analysis like this. 

### Your Intended Stakeholder

This is actually one of the hardest parts - identifying your primary stakeholder. In the real world, you will know exactly who they are and what is expected of you. Here, you are being asked __to choose__ one (and really try to focus on just one) stakeholder. This will be the audience to whom you address your deliverables (as well as other data scientists on your team, of course!).

## Final Check

Before submitting, confirm that everyone on your team can answer the following:

- [ ] We can clearly describe the problem we will address in our Capstone project.
- [ ] We understand why the problem may matter and __to whom__ it may matter.
- [ ] We have identified a relevant stakeholder or intended audience.
- [ ] We have identified the data we will use and what those data represent.
- [ ] We understand, at a high level, what machine learning and data science practices might contribute to this problem.
- [ ] We have identified any important questions or uncertainties that remain.
- [ ] We have identified, at a high level, any risks to this project.
- [ ] We have confirmed that the project and data source are appropriate for the eight-week Capstone.

__Team confirmation:__ We agree that this charter accurately describes our shared understanding of the project at the start of the Capstone.

__Submitted by:__ [You only need one person to submit]

__Date:__ [Don't forget to date it!]
