# Abstract
**Background:** DevOps (Development and Operations) and Continuous Integration/Continuous Delivery (CI/CD) practices have been increasingly adopted within the software industry. CI has become an integral part of modern software development practices, contributing to the early detection of integration issues, reducing the likelihood of conflicts, bugs, bad performance, and unexpected behaviors, and enabling teams to deliver software more rapidly and reliably. However, the reality in industry practice shows a lack of visibility into CI pipelines, which hinders deviations and bugs.  
**Aims:** This repo presents a cloud-agnostic process to gain visibility in CI pipelines to provide teams with a comprehensive set of CI-specific metrics, thus supporting objective monitoring and observability of the quality and efficiency of CI workflows and decision-making processes. 
**Method:** This API defines a process to retrieve some key performance indicators (KPIs) of CI operations, such as the type of validation/tests/action performed, time consumed, results, structured reports, code change references, and context details like  integration environment, addons (e.g., sidecars, plugins, databases, bypasses, and independent software) and CI tool versions.  
**Results:** We identified a set of metrics in the CI pipeline that provide an objective understanding of the efficiency and quality of the CI workflow. The result is a cloud-agnostic process supported by a REST API that recollects and retrieves data using querying and transformation to observe the CI KPI data.  
**Conclusion:** CI is heterogeneous due to the diversity of pipeline platforms, repositories, checkers, and integration environments. This solution homogenizes CI KPI data in a (semi-)structured way to localize errors and trends to make data-driven decisions better.
# Introdution
Continuous integration (CI) has a broad impact on improving software quality and reducing risks. Humble, Farley, and Duvall expanded this term to CICD in [Continuos Delivery](https://www.oreilly.com/library/view/continuous-deployment/9781098146719/ch01.html) and they popularized both. Although other authors, such as [Beck & Andres](https://dialnet.unirioja.es/servlet/libro?codigo=715107) previously introduced the need to build every day, the CI term seed. All of them emphasized the importance of regularly integrating code changes, automated testing, and continuous feedback loops to improve software quality, reduce risks, and improve team collaboration. CI promotes the validation of new code contributions each time a new code contribution needs to be merged. This validation is performed regularly with a set of checkers, tests, artifact builds, artifact pushes, among others.

Today, CI cannot be separated from automation. Developers perform manual tests in their local framework, but they need to rely on an automatic integration pipeline that performs all the required steps to validate and verify new code contributions from new or changing features. Automated executions of CI pipelines successfully pass (or fail) code contributions based on automated steps for compiling, testing, verification, and validation. 

After executing a CI pipeline, a reviewer should look into the code to do an abstract check, that is, verify whether the code satisfies the minimum product value defined in the feature, the code is maintainable, and the computational resources are efficiently used, among others. However, very often, reviewers observe the code based on prejudges instead of objective data. It would be desirable, for example, that reviewers could check the code performance in the past based on the latest executions, as many CI executions with high-value data based on different code behaviors over time could be available. This could help reviewers and managers to have a clear picture of the current trends of the integration process and the development project.

We can state that the mental load of reviewers, assessing whether the proposed contribution fits well with the base code without structured and accessible data of the code and CI executions, is not scalable. The reality in industry practice shows a lack of visibility and observability in CI pipelines, which hinders deviations and bugs, partly motivated by the fact that CI data originate from multiple heterogeneous sources. Thus, although CI is today a mature work philosophy,  CI observability and visualization are required to reduce bad practices, improve performance, and even detect code anomalies.

From this point on, it is necessary to empower the CI conception into a more useful work philosophy by designing a comprehensive set of CI-specific metrics to enable observability and alerts over the continuous integration flow. To that end, this project presents a cloud-agnostic process for storing semi-structured CI data (because each CI operation has its peculiarities) as well as CI metrics to make data-driven decisions and avoid bias when code contributions are integrated and reviewed. It could be fundamental to detect trends in CI operations (e.g. performance), trace the versions of the tools used, collect data from different validation reports, correlate them, and compare the performance under different cloud environments, mocks, or even add-on versions.

# Background and related work
Before presenting the research methodology, let me introduce some concerns and key concepts around CI  that are going to be a pillar of this work.
This section discusses some of the key concepts around CI.

## CI as support for Code Reviews
CI is a key supporting strategy in code review to automatically analyze whether new code contributions meet the minimum standards of the project. It is commonly used as the first filter before a human spends time performing a code review. This can be considered the main goal of CI. There are already works explaining this 
 
The article: [The silent helper: the impact of continuous integration on code reviews](https://research.tue.nl/en/publications/the-silent-helper-the-impact-of-continuous-integration-on-code-re) asserts that CI reduces internal discussions in teams. In their work, the authors empirically revealed that after CI implementation, the code contributions had fewer review comments. They focus on CI as a time-saving improvement and amount of effort. However, they do not focus on one point that we consider the most important, i.e., the mental load, probably because it is difficult to empirically calculate it. CI reduces a high mental load during code review. If developers and reviewers had fewer things to take into account during the contribution process, they would be more open to finding lines of improvement because the CI machinery automates a multitude of validations that humans do not have to be aware of.

 

## CI Issues

CI automates some validation processes that relieve code stakeholders of the mental burden. However, CI pipelines are code that is programmed to validate other code. We cannot rely on CI (and their validators) as perfect tools to validate code. CI also contains bugs, bad performance, bad behaviors, antipatterns, and even bad trends, aka. bad smells. CI validations evolve in the same way that the base code evolves over time. Next, we summarize some studies on the behavior of CI and possible bad smells.


The paper [Do Developers Fix Continuous Integration Smells?](https://dl.acm.org/doi/10.1145/3617555.3617870) describe the smells of CI and focus on their antipatterns. The conclusion of this paper indicates that CI is not commonly fixed for unwanted behavior. The paper proposes to study the reason for poor CI maintainability in future work. This software is the next step because it provides with CI observability that enables one to find bad smells easily.  

The paper [Test Flakiness' Causes, Detection, Impact and Responses: A Multivocal Review](https://www.researchgate.net/publication/366005041_Test_Flakiness'_Causes_Detection_Impact_and_Responses_A_Multivocal_Review) analyzed Flaky tests, their causes, detection, impact, and responses. A flaky test is a non-deterministic test that means that with the same input, the outputs can be different. The flaky test causes are the following: dependency order, random variables, network dependencies, datetime variables, hardware, external dependencies, environment dependencies, platform dependencies & concurrent flows. Considering this, it is possible to detect if a validation is deterministic or not. It is important to avoid the previous causes to reduce the mental load and workload of dealing with flaky tests, but sometimes it is impossible due to the test complexity. The no-deterministic test exists and they are more common in integration testing, end-to-end tests, or non-functional tests than in other CI validations. According to the paper, flaky tests have an impact on testing, product quality, debugging, and software maintenance. 

## CI observability tools

After making clear that CI is a kind of *watchman* that prevents issues in the base code and even reduces the mental load, and is a time-saver for many workflows during software development, it is also clear that CI is required to be maintained. At this point, we can ask ourselves... Who watches The Watchman?


[Towards a Fully Automated System for Testing and Validating NetApps](https://www.researchgate.net/publication/362076165_Towards_a_Fully_Automated_System_for_Testing_and_Validating_NetApps) proposed a telecommunications architecture in their Horizon 2020 European [5GASP](https://www.5gasp.eu/) project, and a component called CI/CD Manager that stores all test results to be displayed later in a visualization dashboard. This component is coupled with their software solution; however, it is a good approach to observe how the network services' behavior evolves over time.

[Monitoring a CI/CD Workflow Using Process Mining](https://www.researchgate.net/publication/354426180_Monitoring_a_CICD_Workflow_Using_Process_Mining) explains how data mining can add visibility to developers' teams in an e-commerce platform. They present a process to observe the CI/CD workflow using Kafka to improve the team's performance and avoid flow errors. However, they do not focus on the code validations or deployment validators. They are very focused in their case study Way of Working structured by different environmental purposes. This scope is closed for this case study because they have a coupled solution and the metrics they collect do not describe the code status over time. This is one of the consequences of collecting logs instead of metrics.

[QEX: Automated Testing Observability and QA Developer Experience Framework](https://ieeexplore.ieee.org/document/10132252) presents software, which is a QA framework to integrate testing data to enable testing observability. The framework implementation relies on a specific technological stack: InfluxDB as a time-series database, Grafana as a monitoring solution, Jira as project management, Gitlab as a version control system, and Jenkins as an automation server. Quality assurance focuses on ensuring the overall quality of the software product meanwhile CI aims to improve the efficiency and reliability of the development process by automating the integration and testing of code changes.

There are also commercial solutions like [Datadog CI Pipeline](https://www.datadoghq.com/product/ci-cd-monitoring/). They provide an observability platform to improve the reliability of CI pipelines. However, their solution is not open to any kind of CI/CD tool and the scope is to observe pipelines itself, not validations. As we know a pipeline can be composed of 1 to N validations because it depends on the project CI strategy.

# A PROCESS FOR OBSERVABILITY OF CI WORKFLOWS

## CI taxonomy
Each software project relies on different programming languages, different frameworks, and different tools to guarantee continuous integration. All the CI operations have useful data like the commit-id, the branch, the execution start time, the duration, the tool used for the operation and the version, the operation result, in addition to others. This data for each operation is going to be defined as CI KPI. Each commit has a list of KPIs that specifies if it has passed the validation or not and all the context data described above.
![CI_KPIs](https://github.com/user-attachments/assets/7262bd92-651e-41f5-91fa-34da0654d47b)
### Heterogeneous execution environment
Many execution environments should be traced with the CI operations. The environment can be a reference to a specific CI solution or specific hardware resources for CPU cores, RAM, memory, GPU, or network characteristics. The same CI operation with different CI execution environments can be different in time duration or even in results as has been explained in the CI Issues section.

### Heterogeneous operations
Each repository has different languages or framework specifications. The testing scope depends on the project. Some operations validate the code, others store artifacts, and others are in charge of managing the versioning. In this repo, we are interested in the validators because: 

* They are the reason why the commits are rejected automatically
* Some validators can score the software implementation
* The validators "take a photo" of the current code behavior


### Group the CI tools by target:
The validations can be grouped into Code Linters, Unit Tests (UT), Integration Tests (IT), End to End Tests (E2E), and Non-functional tests (NFT).
Each commit will have a list of KPIs that measures their performance and behavior with the following cardinality:

* Lint: 0..N Because a repository can have multiple file types. Examples: .java, .py, .yaml .containerfile
* UT, IT, and E2E: 0..1 Because the tests are executed over a test suite.
* NFT: 0..N Because each quality attribute that a project needs to satisfy can be tested using even multiple tests.

## Deterministic and non-deterministic test
Some tests had different results with the same "inputs", they are called Flaky tests.
Those tests are seen as a weakness (And probably in most cases they have a deterministic solution). However, the real weakness is to have only deterministic tests in a complex system. Flaky tests guarantee that the software is pseudo-deterministic in most cases. Also, they can be useful if the non-deterministic causes can be parameterizable (like environment dependencies for instance) to analyze the change's impacts.

The classification of the previous CI tools by target can be the following:

* Linters: Deterministic because it checks syntactic \& semantic correctness without depending on the flaky causes
* UT: Deterministic because the possible flaky causes are mocked to obtain static results.
* IT: Deterministic or non-deterministic because some causes can be mocked, but others not. It depends totally on the testing scope.
* E2E: Non-deterministic because at least end-to-end tests rely on the network and external dependencies. In addition, E2E can be quite useful to verify some possible flaky causes like environment or platform dependencies.
* NFT: Deterministic or nondeterministic because it depends totally on the quality attribute dependencies to test.
    * An example of a deterministic non-functional test is performing a security test to check the ports exposed by a service and the behavior is commonly pre-configured.
    * An example of a non-deterministic non-functional test is a stress test that can saturate the network or the hardware.

## CI DIKW
The DIKW levels (Data, Information, Knowledge, and Wisdom) of the famous pyramid were introduced by [Ackoff](https://www.researchgate.net/profile/Rob-Keller/post/Original_paper_of_From_data_to_wisdom_by_Ackoff_1989/attachment/63f67d8997e2867d5081d0de/AS%3A11431281121841684%401677098376991/download/Ackoff89.pdf)
The concept had existed before, however, Ackoff was the first "original articulation".

CI data can fit this model and its hierarchies:


* Data: These can be simple results or context values. Data is the most objective hierarchy stage
* Information: it is the result of composed data (contextualized, categorized, calculated, corrected or/and condensed). This stage loses objectivity from data because it is composed from the point of view of specific stakeholders. This is the stage that we reach in a CI KPI document.
* Knowledge: it is the result of comparing, adding consequences, or/and making connections with other Information. This stage loses objectivity from information due to we apply transformations with other info. This is the stage we can reach querying and doing transformations to the available documents and personal bias.
* Wisdom: it is the stage action-oriented that measures the knowledge hierarchy previously reached to make wiser decisions. This is the most subjective stage due to we inherit previous subjectivity and we perform a stakeholder decision.


During this DIKW process, we lose objectivity at each stage we advance. However, that is not necessarily negative because the stakeholder decision risk is lower (based on his bias). To illustrate this statement we can mention the philosopher Immanuel Kant (Immanuel Kant. (1998) [1787]. The Critique of Pure Reason. Cambridge University Press [p.~110-111]), since he drew a parallelism between the "Copernican revolution" and his epistemology studies. His parallelism revolves theoretically that (a) knowledge must conform to objects to the postulation that (b) objects must conform to our *a priori* knowledge.
![DIKW](https://github.com/user-attachments/assets/e76533fc-b300-41e0-87d6-71b79f486083)

## Software architecture
The proposed architecture is based on a REST API in charge of collecting CI KPIs, and retrieving and removing KPIs in case of error. A REST API has clear interfaces to be tech-agnostic for many cloud-native environments.

![Arch](https://github.com/user-attachments/assets/4184bb0d-0b81-4e42-8be5-0e0694236079)


The KPIs are stored as a JSON object.

On the one hand, the interoperability between the REST API and the CI machinery is performed by an HTTP POST request from the CI side. In a POST request, the CI tool populates a JSON document with the structure defined in JSON-schema

On the other hand, the connection between the REST API and the observability is performed by an HTTP GET request from the observability side. In GET request, the Observability tool retrieves the expected data querying and transforming the data.

### Data validation model
During the section CI-taxonomy it has been described that CI tools, the execution environment, and the CI operations are heterogeneous.
The effort to homogenize all the particularities has been specified in a data model.
As the KPIs are semi-structured data (due to they are JSON data), they can be validated syntactically and semantically through JSON schema using a data model that requires at least the following keys, and the values types.

![json-schema-deps](https://github.com/user-attachments/assets/6553dab4-543e-4160-b18f-8eb137c0faae)


Some schema keys are not primitive values. Context key is an object that indicates the validation tool used, the tool version, and the environment that could be a string indicating the identifier (for example Circleci) or another object to specify the hardware resources.
Addons is a list of 0 to N elements, and each element has an identifier name and a specific version associated. 
The result key has a value that can be a boolean in case of simple validation operations, a string in case of output logs, or an object in case of validation reports.

## Implementation
This implementation called CI-KPI is a REST API developed in Python3 and [FastAPI](https://fastapi.tiangolo.com/) web framework.
The implementation counts with 3 endpoints that satisfy CRUD operations:

* GET to retrieve CI-KPI data explained in detail in \ref{Get-implementation}
* POST to upsert the CI KPIs. In this endpoint, it is necessary to fit the JSON schema described in \ref{json-schema}
* DELETE to remove CI-KPIs


### Query and data transform language

To improve the data retrieval from the database to the observability system some strategies have been placed.

* Querying: to not retrieve all the possible data it is possible to filter by the keys/values described previously
* Projection: to not retrieve the entire CI-KPI object, it is possible to select only the keys you want to retrieve to reduce the complexity of the data and reduce the network data traffic.
* JSONata: using the [JSONata](https://jsonata.org/) language it is possible to do data transformations to reach the data structure you desire to be visualized in the observability tools.

# Discussion and Implications

The CI issues described indicate that CI is in a vulnerable position. CI is a software development practice that is rarely maintained and more rarely observed. Supervising the CI tools and their operations is necessary to prevent malfunction and bad performance. 
As it has been seen in code review, CI reduces time, an amount of effort, and mental load. However, If a CI is not well maintained CI can be useless or even a disadvantage.

It seems that this vision is partially shared by the different references in CI observability tools. All of them see the necessity of watching the watchman(CI system).

However, the current approaches are quite coupled to their CI and observability systems, impeding incorporation into any kind of system. In addition, there is a lack of:

* Validation tools and their version's traceability
* A standardization of expected results
* Addons references and versions (like sidecars, plugins, databases, bypasses, independent software, third parties, or mock services)
* Identification of determinist or non-determinist tests based on the flaky test causes.
* CI environment execution details that can be crucial for mixed cloud projects or to study cloud migrations.

The implications consist of describing a process, coded in a cloud-agnostic tool to start observing the CI operations in any kind of project framework. It has identified and grouped the common validators and identified the CI pain points to reach the knowledge stage in the DIKW CI pyramid.

* Reaching the Information stage contextualizing, categorizing, calculating, and structuring the CI data when the CI machinery fills up a payload following the structure mentioned in JSON-schema to the POST request specified in CRUD to store a CI KPI.
* Acquiring the knowledge stage by comparing, adding consequences, and making connections above the CI KPIs stored in the API using the querying and transformation utilities described Get implications

After the Knowledge stage, based on the stakeholder bias, it is possible to make data-driven decisions that could improve the project performance significantly.

# How to start
You need a MongoDB instance to store your CI KPIs.
An then, you only need to run:
```bash
docker run -p 80:80 -e MONGO_URI='<URI>' ubiquitycloud/ci-kpi
```
