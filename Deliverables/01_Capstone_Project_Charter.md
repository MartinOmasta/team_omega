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

__Project title:__ Norwegian Heating - It's Electric! Customers as routine Creatures-of-Habit or as Homo Economicus - driven by rational self-interest

__Team name:__ ![Team Omega's Logo](https://github.com/MartinOmasta/team_omega/blob/main/images/Team_Omega_Logo_Small.png) Team Omega ![Team Omega's Logo](https://github.com/MartinOmasta/team_omega/blob/main/images/Team_Omega_Logo_Small.png)

__Team members:__ Anthony Ruoti, Benjamin Niemi, Martin Omasta <br>
- Facilitation/Team Lead: Martin (Sprint 1)
- Notetakers/Document Lead: Ben (Sprint 1)
- Delegate/Communications Lead: Anthony (Sprint 1)

__Project source:__

- [x] Capstone Curated Project Bank
  - A rich dataset of hourly residential electricity consumption data - https://github.com/ksgeist/dse6311_capstone/tree/main/Capstone_Project_Bank/Electricity_Pricing
  - Norwegian Krone to US Dollar exchange rates - https://www.exchangerates.org.uk/NOK-USD-spot-exchange-rates-history-2020.html
  - Team Omega Github Repository: https://github.com/MartinOmasta/team_omega 

- [ ] Alternative project approved by instructor

### Problem and Context

__What problem are you trying to address?__

Describe the problem in a few sentences. What is happening that an organization, business, agency, or community would want to understand, predict, or improve?

*Example:* A subscription-based company is experiencing customer attrition. When customers cancel their subscriptions, the company loses recurring revenue and may incur additional costs to acquire replacement customers.

__Your response__: 
- Which households shift electricity use in response to variable pricing, and can we predict their flexibility? <br>
    Customers are given notifications regarding how the pricing on a particular day will be calculated. These can change daily, and are often times fluctuating throughout the day. Customers also experience days when the pricing is the default from their provider - acting as a control. There is never really any extended periods of time when a customer can "get used" to how the prices are going to be, and therefore no way for them to develop a routine around how best to activate or deactivate their appliances. 
- We decided to use the prompt question as our base, and contextually flesh out the results with the additional questions listed below.<br>
    Beyond flexibility, might we be able to model future electricty consumption?

### Why Does This Problem Matter?

Briefly explain why the problem is important in its organizational, business, healthcare, public sector, or other applied context. You do not need to provide a literature review or fully support your rationale with sources yet; you will develop the background and rationale during Sprint 2.

__Consider__:
- What consequences might result from this problem?
- Why might an organization or stakeholder want to address it?
- What decisions could a better understanding of the problem inform?

*Example:* Understanding customer attrition could help a company evaluate its retention strategies and determine where to focus customer support or engagement resources.

__Your response__: The problem presented above are related to heating during Norwegian winters, the cost of heating and the reliance on electricity are of utmost importance for the health and wellbeing of specifically the Norwegian residents, though possibly applicable to colder climate countries at large. As many nations begin pivoting from carbon heavy fossil fuels to more renewable energy sources it is important to investigate the topic of the cost of energy itself, and as this is in one of the more inhospitable winter climates - this data can share important insights. If the power is unreliable or too expensive then the populace at large could be harmed during this pivot, energy suppliers will need to take this into account when they move energy prices and influence policies. The insights from this data will inform pricing decisions for power suppliers and have an effect on revenue.

### Stakeholder and Intended Use

__Who would care about the results of this project?__

Identify the primary stakeholder or intended audience. This could be a business unit, organizational decision-maker, public agency, healthcare provider, or other group.

__Primary stakeholder:__

__What might this stakeholder want to learn or do with the results?__

*Example:* A customer retention team might use the results to better understand which customer characteristics or behaviors are associated with cancellation and to inform future retention strategies.

__Your response__: 
- Government: The effects that policy will make on the constituents and how best to guide that forward, keeping in mind the health and well-being of the populace. 
- Electric companies: Who want to maintain a customer base and keep houses heated, maintain affordability and profitability. Who want to maximize profit by increasing price without losing demand due to dimishing returns.
  - Statnett SF, Gudbrandsdal Energi, Ishavskraft, and Bodø Energi
- Populace: Gain information to use for more informed residential, business, and political decisions. 


### Data Overview

__What data will you use to investigate the problem?__

Identify the dataset and briefly describe what it contains. For a project from the Capstone curated project bank, use the information provided in the project description. Remember, you have the option to refine the project goal or question while still using the same data source!

| Item | Description |
|---|---|
| Dataset name | A rich dataset of hourly residential electricity consumption data and survey answers from the iFlex dynamic pricing experiment. |
| Data source | https://doi.org/10.5281/zenodo.8248802 |
| Unit of analysis (e.g., customer, transaction, patient) | Electricity usage in kWH during Norwegian Winters |
| Approximate number of observations, if known |  13.52 Million. |
| General types of information available | Participant ID, Date, Hour of the day, Participation in phase, kWH Demand, Price Signal, Temperature recordings, Household Income, Level of Energy Consciousness, Dwelling Type, Household Size, Appliances Used, EV Availability, Solar Capacity, Habitation Frequency, Life Cycle |
| Data access confirmed? | Yes |

__How might these data help address the problem?__

Briefly explain what information in the dataset could be relevant to the problem.

*Example:* The dataset contains customer demographics, subscription information, service usage, and cancellation status. These data may help the team examine patterns associated with customer attrition.

__Your response__: As this is real world recorded data from a study with the citizens of Norway participating it lends itself to a high level of interest. Norway is a high latitude country which experiences harsh winters with extremely low temperatures. Heating is a crucial issue for those individuals living there and with the prevalence of electric heaters it's very useful to have a data set that measures the usage, along with a variety of pricing experiments and surveys to understand the thoughts of the citizens. The extensive surveys provide insights into customer's life styles, wealth & demographics, attitude toward taking measures to make adjustments to their electrical consumption, descriptions of the home, appliances, service usage and more. All of these data will directly be relevant to determining why factors may make a customer be more flexible.



### The Data Science Opportunity

__What could data science / machine learning / AI practices help you accomplish here?__

At a high level, describe what you hope to learn or accomplish using the available data. You do not need to specify particular algorithms, preprocessing steps, or evaluation metrics here; those belong in the Analysis Plan due in Sprint 2.

*Example:* The team could use historical customer information to identify patterns associated with churn and investigate whether customer cancellation can be predicted using available customer characteristics and behaviors.

__Your response__: Ideally using this dataset to find out how price experiments changed the electrical habits of the participants. 

These data give us an opportunity to form classification typology from discrete behavioral clusters:
- The Optimizers (Homo Economicus) who are highly responsive and excel at rapid load shifting.
- The Inelastic (Creatures-of-Habit) who have a fairly flat response to Pricing Signals told to them by thier power provider.
- The Constrained: These are folk who are willing but may be physically unable due to poor home insulation, infrequent habitation of the dwelling during fluxation, or busy lives to not consider daily reprogramming of the smart thermostat. 

These data also give us an opportunity to form a regression model to predict some type of Flexibility Propensity Index for a given upcoming price shock. We may also be able to model predicted future electricity consumption.


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
4. Phase_1 (From 11 Feb 2020 until 9 Mar 2020) was truncated due to COVID, so much of the data that is available is only from Phase_2 (16 Dec 2020 - 25 Mar 2021)

### Your Intended Stakeholder

This is actually one of the hardest parts - identifying your primary stakeholder. In the real world, you will know exactly who they are and what is expected of you. Here, you are being asked __to choose__ one (and really try to focus on just one) stakeholder. This will be the audience to whom you address your deliverables (as well as other data scientists on your team, of course!).

__Your response__: 
Statnett SF - the state-owned Norwegian transmission system operator is the primary entity that initated, benefited from, and financed this study. This is our primary intended stakeholder and the audience we will address.

## Final Check

Before submitting, confirm that everyone on your team can answer the following:

- [X] We can clearly describe the problem we will address in our Capstone project.
- [X] We understand why the problem may matter and __to whom__ it may matter.
- [X] We have identified a relevant stakeholder or intended audience.
- [X] We have identified the data we will use and what those data represent.
- [X] We understand, at a high level, what machine learning and data science practices might contribute to this problem.
- [X] We have identified any important questions or uncertainties that remain.
- [X] We have identified, at a high level, any risks to this project.
- [X] We have confirmed that the project and data source are appropriate for the eight-week Capstone.

## Works Cited

- M. Hofmann and T. Siebenbrunner, “A rich dataset of hourly residential electricity consumption data and survey answers from the iFlex dynamic pricing experiment,” Data Brief, vol. 50, p. 109571, Oct. 2023, doi: 10.1016/j.dib.2023.109571.
- Google, Virtual Assistant (VA), "Prompt used to generate response (Various prompts "Thoughts on Data Exploration and conceptualizing Flexability")," 2026. [Online]. Available: VAMMA (Virtual Assistant with Manual Modification and Arrangement, Gemini, Google). [Accessed Nov 2026].
- “Homo economicus,” Wikipedia. Oct. 04, 2026. Accessed: Nov. 02, 2026. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Homo_economicus&oldid=1378415223
- “Norwegian Krone (NOK) To US Dollar (USD) Exchange Rate History for 2020.” Accessed: Nov. 02, 2026. [Online]. Available: https://www.exchange-rates.org/exchange-rate-history/nok-usd-2020

__Team confirmation:__ We agree that this charter accurately describes our shared understanding of the project at the start of the Capstone.

__Submitted by:__ Benjamin Niemi

__Date:__ 03 Nov 2026
