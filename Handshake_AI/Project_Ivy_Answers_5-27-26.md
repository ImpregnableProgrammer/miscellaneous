# Project Ivy Project Assessment Answers

8 OPEN RESPONSE QUESTIONS!!!

## Question 1
```
You're running Model A on the tq task. During Stage 1, the model produces code that handles job adding, running, listing, and showing — but the retry logic only attempts the job once instead of blocking through all 3 retries.
 
The continuation criteria states: "Once the tq tool can add, run, list, and show jobs with working dependencies, blocking retries (3 attempts, 5 seconds apart), and cascading cancellation when a parent job fails, move on."

The model declares it's finished and asks if you'd like to proceed to the next feature. What do you do? Walk through your decision step by step.
```

Since the continuation criteria clearly aren't satisfied, I would clearly indicate to the model the incorrect behavior ("the tq implementation retries a failing job only once instead of the expected 3 times, 5 seconds apart while blocking") in my next prompt before allowing it to proceed to the next feature to give it a chance to fix the issue. If the model is able to fix the issue in a few more prompts, I will allow the model to proceed with implementing the stage 2 feature, and immediately note the error and correction in my session notes. Otherwise, if it ends up taking too many more re-prompts (i.e., more than 4 or 5), too long (more than twice the expected time for the session), or the model ends up getting stuck, I will abort the session and immediately note the issue, and then move on to performing the task with model B. In either case, I will report the outcome in my evaluation once I'm finished working with both models. And in any case, if there's an API timeout or external failure, I will start over from an entirely blank slate with the same model and retry from stage 1.

## Question 2
```
During the Model B run, the model implements retry and it works correctly on the first attempt — 3 retries, 5 seconds apart, blocking. However, it hasn't implemented cascading cancellation yet.

Your Stage 1 Planned Interactions include:
• If: Retry only tries once → Say: "The retry isn't working correctly..."
• If: Retry does 4 total attempts instead of 3 → Say: "The retry count is off..."
• If: Retry logic is working correctly → Say: "When a job fails after all retries, any job that depends on it should be automatically marked as cancelled."

Which trigger(s) apply? What do you send? What would be wrong to do here? List as many mistakes as you can. 
```

Since the model implemented retrying as intended (3 retries, 5 seconds apart), the first two triggers do not apply in this case. However, because retry works but cascading cancellation wasn't implemented, meaning jobs that fail after 3 retries don't result in dependent jobs being automatically marked as cancelled, the third trigger applies here, so I would immediately ask the model to implement cascading cancellation as specified for the third trigger, and note the interaction and its outcome in my session notes. I would NOT move on without allowing the model to implement the missing feature, would NOT ask the model to do anything beyond what is specified for the third trigger, would NOT send anything regarding the first two triggers (since they do not apply here), and would NOT engage in any of the planed interactions with model A if they do not apply there.

## Question 3
```
You scored Model B's Correctness as 2/3 on the tq task. Here's what you wrote:

"The core queue operations (add, run, list, show) function correctly, and dependencies are properly created. The priority ordering system correctly routes high priority jobs before normal ones. The blocking retry requirement is fully implemented using a while loop that keeps the execution within a single run call, properly applying a 5-second sleep between attempts. Finally, cascading cancellation correctly recursively updates all dependent jobs to a cancelled state if a parent job exhausts its retries. The final code structure successfully delivers the requested task queue behavior."

A colleague says: "This reads like a 3/3, not a 2/3." Are they right? What's wrong with this rationale, and how would you rewrite it?
```

Yes, the colleague is correct. This rationale does NOT indicate any incorrect behavior's in model B's implementation (i.e., aspects not correctly implemented as expected or indicated by the prompt and any continuation criteria) that merits a 2/3 correctness score instead of a 3/3. So I would add any incorrect aspects of the final implementation that merit a 2/3 correctness score. It also irrelevantly states how the blocking attempt was implemented ("using a while loop that keeps the execution within a single run call"), so I would remove that segment. 

## Question 4
```
You select a preference of +2 (moderately prefer Model B). In your rationale, you write: "Model B was a little bit better than Model A at handling the retry logic, though both struggled."

The dimension scores are:
• Model A: Correctness 1, Agent Behavior 1, Communications 2
• Model B: Correctness 2, Agent Behavior 2, Communications 2

Is there a problem? If so, explain what it is and give two different ways to fix it.
```

Yes, there is a problem. The rationale as written is too short and vague, providing no specifics justifying the preference score and how exactly the models struggled. The rationale can be made better by mentioning specific aspects of each model's behavior (in particular, how exactly they struggled) and final implementation (such as how exactly model B was better at handling the retry logic), and providing a more careful comparative analysis of the models in terms of their dimension scores and other relevant aspects.

## Question 5
```
You uploaded screenshots for both models. But your rationales describe the code's behavior in abstract terms — 'the retry logic handles 3 attempts correctly' and 'cascading cancellation propagates through the dependency tree.' You never mention actually running the tool yourself.

A colleague reads your rationales and asks: "Did you actually test this, or are you just describing what the code looks like?" How do you avoid this problem? 
```

To avoid this problem, I would specify exactly what I did to test the retry logic (such as deliberately creating a failing job that fails across 3 retry attempts and there being a 5 second wait between each retry, with code supporting the existence of the wait) and test cascading cancellation (such as creating a job dependent on a failing job and ensuring that the dependent job is marked as cancelled once the job it depends on fails). I would then attach screenshots of me running these tests with the tool as it was implemented to support my statements.

## Question 6
```
During Model A's run, 3 triggers fired: (1) retry only tries once, (2) off-by-one with 4 attempts, and (3) retry working correctly — so you sent all three prescribed reactions. But in your Trigger Documentation for Model A, you only wrote about Triggers 1 and 2. You forgot Trigger 3.

During Model B's run, Trigger 1 fired (retry once), and after the fix, Trigger 3 also applied (retry working correctly). In your Trigger Documentation for Model B, you only documented Trigger 1.

Why does this matter? What should the Trigger Documentation contain?
```

This matters because if trigger 3 applying in either case isn't mentioned in the trigger documentation, it can't be verified whether I had asked the model to implement the feature or if it just implemented it itself (in the case the feature ended up being implemented), and whether the models were even at all asked to implement the cascading cancellation feature in the final implementations. ALL planned interactions (especially those pertaining to features that must be implemented) should be documented in the trigger documentation to ensure that each session was actually executed exactly as intended with the models having a fair chance to implement all the expected features, so that the models aren't unfairly marked down if the feature didn't exist due to the user failing to mention it rather than the model failing to implement it after being asked to. And it's especially important to mention trigger 3 in this task since it pertains to implementing a feature that wasn't specified in the initial prompt.

## Question 7
```
Here are two Agent Behavior rationales from the tq task. Read both and evaluate their quality.

Model A (score 1/3):
"The prompt clearly defined the requirements. The model skipped one of them. And when trying to fix it, it introduced another one. And it never tested whether a single run call blocks through the retries and it never verified the attempt count was exactly three. A competent model would look at its own logic before presenting the solution — while current_retry <= max_retries with max_retries = 3 starting at 0 produces four iterations, which is easily verifiable. Instead, the model required the user to help with it."

Model B (score 2/3):
"The model made surface-level changes rather than implementing the retry feature meaningfully. When the user gave a specific requirement for retries, it appended a sleep call without reconsidering the control flow structure. It never self-tested the retry path — if it had, it would have noticed the sleep was unreachable dead code. The model treated the retry part of the user prompt as an isolated edit request rather than maintaining a coherent understanding of the full system. However, cascading cancellation and the priority feature were both approached with correct structural thinking, showing the agent was capable of reasoning well."

Which rationale is stronger? What works well in each? What could each one improve?
```

The agent behavior rationale for model B is stronger since, unlike the rationale for model A, it gives specifics supporting some of the claims being made (such as the model "append[ing] a sleep call without reconsidering the control flow structure" for the claim of the model "[making] surface-level changes rather than implementing the retry feature meaningfully"). The rationale for model B also mentions other features (cascading cancellation and priority) being approached correctly unlike the rationale for model A, which simply focuses on the retry logic not working in a single case and doesn't elaborate further as to whether the model addressed the problem (or whether the user even asked it to) and doesn't even consider whether any other features were approached correctly. The rationale for model A effectively fails to substantiate upon much of its claims (such as failing to making it clear exactly which requirement was skipped and whether it was the fault of the user or the model, and exactly what other defect was introduced) and fails to specify whether the user did anything beyond reading the code to make their claims, only mentions negative aspects, and pins much of the blame on the model rather than acknowledging the possibility of user error in guiding the agent's behavior. In essence, the agent behavior rationale for model A comes across as much more negatively-biased, shallow, and vague than the rationale for model B, and as a result fails to fully justify its score of 1/3. However, the rationale for model B can still be improved by elaborating upon what exactly "correct structural thinking" means with specific examples.

## Question 8
```
Walk through the complete Model A run on the tq task from start to finish. Assume:
1. You send the Stage 1 prompt. The model builds tq but retry only tries once.
2. You send the Trigger 1 reaction. The model fixes retry but does 4 attempts.
3. You send the Trigger 2 reaction. The model fixes it — retry now works.
4. Trigger 3 applies. You send the cascading cancellation reaction. The model implements it.clean 
5. All Stage 1 criteria are met. You send the Stage 2 prompt.
6. The model implements priority. Stage 2 criteria are met. Session is done.

What is the complete sequence of actions and uploads from the moment the session ends to the moment you're ready to start Model B?
```

Now I must upload the zip archives I should've created (with "zip -r") of the working directory before and after working with model A, any supporting screenshots I took while working with the model and of the final output, and (after quitting the model A interface) the exported trajectories generated by running "./scripts/export.sh". I must also document the 3 triggered interactions and whether the continuation criteria were met in the trigger documentation for model A in Handshake AI. Once I've done all that and sorted through my session notes, I must then clean the working directory (which is done by ./scripts/start.sh) and create a zip archive of it before beginning to work with model B.
