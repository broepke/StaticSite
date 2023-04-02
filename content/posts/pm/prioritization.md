Title: Five Powerful Prioritization Techniques from Product Management
Date: 2023-04-04
Modified: 2022-04-04
Status: published
Tags: design thinking, datascience, innovation, product management
Slug: prioritization
Authors: Brian Roepke
Summary: How Data Scientists can learn from how a Product Manager builds a product, thinks about customer-centricity, and ensures that the product is successful.
Description: How Data Scientists can learn from how a Product Manager builds a product, thinks about customer-centricity, and ensures that the product is successful.
Header_Cover: images/covers/frameworks.jpg
Og_Image: images/covers/frameworks.jpg
Twitter_Image: images/covers/frameworks.jpg

# Product Management Techniques for Prioritization

As a Data Scientist, Analyst, or anyone developing a product or solution, you can borrow tools that Product Managers use to prioritize requirements. With limited resources and time, it's important to focus on the features and requirements that will bring the most value to your customers. Here are my five favorite techniques for prioritizing features and requirements:

1. User Story Mapping
2. Weighted Prioritization Matrix
3. Importance vs. Difficulty Matrix
4. Buy a Feature
5. Kano Model

Each technique has its strengths and situations where they work the best. Try them all and learn when to apply each one.  Let's walk through each of them with some basics on how to perform them and when to use them.

## User Story Mapping

**User Story Mapping** is a powerful technique for visualizing a product's features and requirements through a map. It helps you understand the user's journey and prioritize features based on their importance in achieving their goals.

To perform User Story Mapping:

1. Start by breaking the product into smaller user stories. These stories should describe the user's goals, needs, and pain points.
2. Organize the user stories, the groupings that represent the different activities along the way, and the workflows the user needs to perform to complete that activity.
3. Prioritize the user stories based on their importance to the user journey (top to bottom).

**Tips**: User Story Mapping is an iterative process that should be updated and revised regularly based on user feedback and changing business priorities. Also, involve your team and stakeholders in mapping to ensure alignment and buy-in.

**When to Use**: This method works great when you're starting a new project and want to understand a user's workflow. This method helps you frame the problem, and you will most certainly identify areas you should have thought of.

![User Story Mapping]({static}../../images/posts/prioritization_story.png)

## Weighted Prioritization Matrix

The **Weighted Prioritization Matrix** is a technique for prioritizing features based on multiple criteria. It involves assigning a weight to each criterion and scoring each feature based on how well it meets each criterion. The resulting scores are then multiplied by the weights to calculate a final score for each feature.

To perform the Weighted Prioritization Matrix:

1. Identify the criteria you want to use to evaluate the features.
2. Assign a weight to each criterion based on its relative importance.
3. Score each feature on a scale of 1-n for how well it meets each criterion. You can use any scale you want but keep it consistent.
4. Multiply each score by its corresponding weight and sum the results to calculate a final score for each feature. As a bonus, you can square the score to give higher scores more weight, e.g., the Weighted Sum of Squares.


```python
=($B$1*B3*B3)+($C$1*C3*C3)+($D$1*D3*D3)+($E$1*E3*E3)...
```

Download my Excel Sample here: [Weighted Prioritization Matrix]({static}../../pdf/weighted_prioritization_matrix.xlsx)

**Tips**: When using the Weighted Prioritization Matrix, involve stakeholders and team members in the criteria selection and weighting process to ensure alignment and buy-in. Additionally, be mindful of how you score each feature and try to be as objective as possible. You can mix custom criteria, such as how it fits a specific business goal, with more traditional criteria like risk, revenue, urgency, effort, and more.

**When to Use**: This method is great when you want a more methodical way to score a long list of features. The ability to sort by the final score gives you a stacked ranked list. Because you collaborate with your team on the scoring system, it can remove some subjectivity around prioritization.

![Weighted Prioritization Matrix]({static}../../images/posts/prioritization_weighted.png)

## Importance vs. Difficulty Matrix

The **Importance Difficulty Matrix**, also known as the Value Effort Matrix, is a technique for prioritizing features based on their importance and difficulty. It involves mapping features on a two-dimensional matrix, with the importance of the feature on one axis and the difficulty of implementing it on the other.

To perform the Importance Difficulty Matrix:

1. Identify the features you want to prioritize.
2. Sort each feature on the horizontal axis from least to most important. Make sure no two features are in the same column.
3. Next, sort each feature on the vertical axis from least to most difficult. Make sure no two features are in the same row.

**Tips**: When using the Importance Difficulty Matrix, involve your team and stakeholders in scoring to ensure alignment and buy-in. Additionally, the process of sorting is the most important part, and what you're doing is getting alignment on the priority. Additionally, each feature must be in a different column or row, ensuring that no two features are considered equally important or difficult.

**When to Use**: A great collaborative exercise when you have about ten items you want to sort. This reduced set could be an already filtered list of items you've selected and want to get absolute priority.

![Importance Difficulty Matrix]({static}../../images/posts/designthinking_id.png)

## Buy a Feature

**Buy a Feature** is a technique that involves giving customers a set amount of **money** to **buy** the features they want to see in a product. Customers can allocate their budget to the features they believe are most important. This technique can help product managers understand the most in-demand features among their customers and prioritize them accordingly.

To perform Buy a Feature:

1. Identify the features you want to prioritize. 
2. Assign a monetary value to each feature and give customers a budget of "money" to spend on them. 
3. You can use physical or digital tokens to represent the money and have customers physically "buy" the desired features. Once all customers have spent their budget, test the results to determine which features were most popular.

**Tips**: To ensure the success of "Buy a Feature," set clear rules and guidelines for the process. Be transparent about the budget and how much each feature costs. Make sure to involve a representative sample of your customer base to get a broad perspective. Additionally, consider offering different budgets to different customer segments, as some may value certain features more than others.

**When to Use**: When you work directly with customers or stakeholders, they insist that everything is a high priority. The Buy a Feature technique forces customers to decide what they truly want. It works well with a group of people where you can set the value of really difficult features to be higher than the amount one person is allocated, forcing a collaborative discussion where multiple people need to pool their resources together.

![Buy a Feature]({static}../../images/posts/prioritization_buy.png)

## Kano Model

The **Kano Model** is a technique for identifying which features will provide the most value to customers. It categorizes features into various types:

* **Must-Be**: These are basic requirements that customers expect. These are features such as the brakes on your car, and you wouldn't buy a car without them.
* **Performance features**: These provide incremental value to customers. These features can be better gas mileage or a more powerful engine.
* **Delighters**: These are unexpected features that can provide a wow factor to customers. These features are things like a heated steering wheel or a sunroof.

To perform the Kano Model:

1. Identify customer needs: The first step in using the Kano Model is to identify the customer needs related to your product or service, which can be done through surveys, focus groups, or customer interviews.
2. Categorize customer needs: Once you have identified customer needs, you need to categorize them into three categories: Must-haves, Performance needs, and Delighters.
3. Determine satisfaction levels: Next, you need to determine the satisfaction levels of your customers for each of the identified needs. A Likert scale (e.g., 1-5) can measure customer satisfaction.
4. Plot the data: Once you have the satisfaction levels for each need, plot them on a Kano Model graph. On the horizontal axis, plot the level of performance or implementation of the need, and on the vertical axis, plot the satisfaction level of the customer
5. Analyze the results: Based on the plotted data, you can identify the needs that fall into each category (Must-haves, Performance needs, and Delighters). Additionally, you can identify the needs that are not currently being met and need improvement.
6. Develop an action plan: Based on the analysis, develop an action plan to address your customers' needs involving improving must-haves, optimizing performance needs, or investing in delighters.
7. Repeat the process: The Kano Model is not a one-time exercise. To ensure that you are meeting your customers' needs, it is important to repeat this process periodically to identify changes in customer needs and satisfaction levels.

**Tips**: Remember that customer needs and expectations may change over time, so it's important to reassess the categorization of features regularly. Also, be careful to focus only a little on delighters at the expense of must-haves, as paying attention to basic requirements can lead to customer satisfaction. Additionally, use a large enough sample size when conducting surveys or interviews to ensure that the data represents your customer base.

**When to Use**: This is one of the more comprehensive techniques for prioritization, and it can take a while to get the hang of it. I recommend reading [The Complete Guide to the Kano Model](https://foldingburritos.com/blog/kano-model/) on Folding Burritos.

## Conclusion

Prioritization is a critical skill for anyone building a product. Prioritization requires deeply understanding your customer's needs, business goals, and resources. The five techniques we've discussed - User Story Mapping, Weighted Prioritization Matrix, Importance vs. Difficulty Matrix, Buy a Feature, and Kano Model - offer different approaches to prioritization. Still, all aim to maximize value for your customers and business. Remember to involve your team and stakeholders in the prioritization process, regularly reassess your priorities, and focus on delivering value to your customers. Using these techniques effectively, you can create products that delight your customers and drive business success.
 

*If you liked what you read, [subscribe to my newsletter](https://campaign.dataknowsall.com/subscribe) and you will get my cheat sheet on Python, Machine Learning (ML), Natural Language Processing (NLP), SQL, and more. You will receive an email each time a new article is posted.*

## References

Frameworks Photo by <a href="https://unsplash.com/@dtopkin1?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Dayne Topkin</a> on <a href="https://unsplash.com/photos/Sk-C-om9Jz8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
    