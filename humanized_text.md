CHAPTER 8
Integrating IoT and Wearable Devices with 6G
Philip Michael Asuquo, PhD
Department of Computer Engineering, University of Uyo, Uyo, Nigeria
Email: [philipasuquo@uniuyo.edu.ng]

ABSTRACT
The shift to 6G wireless networks, the Internet of Medical Things (IoMT), and artificial intelligence changes healthcare from a reactive field to a continuous, data-driven practice. 6G targets 1 terabit per second throughput and sub-microsecond latency, which enables new wearable biosensors, remote diagnostics, and telemedicine platforms. This chapter explains the technical foundations of this shift, the necessary architecture, and the relevant security, ethical, and policy issues. Key topics include edge-cloud coordination, remote patient monitoring, explainable AI, and federated learning. Successful deployment depends on technical progress, cross-disciplinary work, regulation, and secure design.

Keywords: 6G networks; Internet of Medical Things (IoMT); wearable devices; remote patient monitoring; edge computing; explainable AI; federated learning; digital medical twins; telemedicine; healthcare security.

TABLE OF CONTENTS
1. Introduction
2. Technological foundations: 6G and smart healthcare
   2.1 6G vs. 5G: Technical evolution
   2.2 Capabilities relevant to healthcare
   2.3 How 6G supports intelligent healthcare
3. Wearable devices and IoMT in healthcare
   3.1 Types and functions of wearables
   3.2 Monitoring, real-time feedback, and data analytics
   3.3 Benefits and constraints
4. Integration models and implementation frameworks
   4.1 Proposed architecture for 6G-IoMT integration
   4.2 Data flow, edge/cloud coordination, and device communication
   4.3 Implementation and scalability challenges
5. Case studies and use cases in diagnostics
   5.1 Remote patient monitoring
   5.2 Individualized AI treatments
   5.3 Telemedicine
   5.4 Solutions to sustainability, data burden, and ethics
   5.5 Real-world exemplars
6. Security, privacy, and ethical considerations
   6.1 Health data risks and security strategies
   6.2 Real-time data transmission safeguards
   6.3 Compliance and ethical AI design
7. Challenges and future directions
   7.1 Technical bottlenecks
   7.2 Research trends
   7.3 Strategic policy and cross-disciplinary collaboration
8. Conclusion
References

LIST OF FIGURES
Figure 8.1 – Application of Wearable Devices in IoMT
Figure 8.2 – Proposed Architecture for 6G-IoMT Integration
Figure 8.3 – Diagram of a 6G-Enabled Smart Healthcare System

LIST OF TABLES
Table 8.1 – Comparison of 5G and 6G Capabilities for Healthcare
Table 8.2 – Key Features, Benefits, and Constraints of Wearable Devices and IoMT
Table 8.3 – Ethical Principles and Compliance Frameworks for AI in Healthcare
Table 8.4 – Security Challenges in 6G-IoMT Healthcare and XAI Mitigation Strategies

1. INTRODUCTION
Healthcare is changing as artificial intelligence, smaller sensors, and new wireless networks develop. Moving from 5G to 6G enables a new model of care. Previous networks helped clinicians inside hospitals, but 6G expands their reach across locations and time.

The Internet of Medical Things (IoMT) includes wearable biosensors, implants, and smart devices that constantly record physiological data. Sending this data over 6G and analyzing it with AI opens new clinical options. Doctors can manage chronic conditions between appointments and detect deterioration early. They can also update treatments based on live data and perform remote surgery.

This chapter explores these uses and their complications. The shift is technically possible but depends on decisions about security, regulation, ethics, and access. The chapter covers 6G technical foundations, wearable devices, integration frameworks, diagnostic case studies, security, and future research directions.

2. TECHNOLOGICAL FOUNDATIONS: 6G AND SMART HEALTHCARE
To understand what 6G makes possible in healthcare, we must look at how it differs from 5G. 6G represents a different network architecture.

2.1 6G vs. 5G: Technical evolution
5G improved mobile broadband and machine communication compared to 4G LTE. However, 5G cannot handle a healthcare system where millions of devices transmit data constantly for clinical decisions.

6G changes this through three main advances:
1. Data rate: 6G targets 1 terabit per second throughput (VDE, 2024), whereas 5G operates in gigabits. This allows simultaneous transfer of large medical images, genomes, and high-resolution video.
2. Latency: 6G reduces communication delays to sub-microseconds. This makes remote surgery feel instantaneous, avoiding dangerous lag.
3. Device connectivity: 6G supports 10 million connected devices per square kilometer, compared to 5G's 1 million. This allows hospitals to connect every room, wearable, and sensor at once (A. K. S. A. Al-Mekhlafi et al., 2024).

Table 8.1: Comparison of 5G and 6G Capabilities for Healthcare
| Capability | 5G Characteristics | 6G Characteristics | Healthcare Benefit |
|------------|--------------------|--------------------|--------------------|
| Data Rate | Gbps range | Terabit-per-second (VDE, 2024) | Image transfer; telehealth |
| Latency | ~1 millisecond | Sub-microsecond | Remote surgery; critical alerts |
| Device Density | ~1 million/km² | 10 million/km² | Pervasive patient monitoring |
| Edge Computing | Supplementary | Native edge/cloud integration | Localized rapid diagnostics |
| AI Integration | Supplementary tool | AI-native network (Rajab, 2024)| Autonomous diagnostics |
| Frequency Range | Sub-6 GHz / mmWave| THz/Optical; up to 100+ GHz | High bandwidth; environmental sensing |
| Network Architecture| Terrestrial focus | Space-air-ground-sea (Kaur, 2025) | Access in remote areas |

6G also introduces new architecture. Terahertz (THz) communication uses high frequency bands for more bandwidth. Massive Multiple Input Multiple Output (MIMO) antennas improve spectral efficiency. Integrated Sensing and Communication (ISAC) lets the network exchange data and sense the environment at the same time (DelveInsight, 2025).

2.2 Capabilities relevant to healthcare
6G performance improves clinical work in three ways.

Ultra-low latency
Delays matter in healthcare. A few milliseconds of lag during remote surgery can cause errors. 6G targets single-digit microsecond delays, enabling the bidirectional control needed for robotic telesurgery and live monitoring.

Massive bandwidth and throughput
Current networks transmit high-resolution medical images with noticeable delay. 6G’s terabit-per-second throughput removes this problem, allowing distant care teams to share complex data easily. This bandwidth also supports extended reality for surgical planning (Rajab, 2024).

Edge computing
6G integrates edge computing, moving data processing closer to the source. Hospitals can run analytics on-site or at the bedside instead of sending data to remote servers. This reduces latency and keeps sensitive patient data within the hospital, lowering interception risks.

2.3 How 6G supports intelligent healthcare
Combining 6G with AI, IoT, blockchain, and digital twins changes care delivery. Systems can gather data continuously and prompt intervention before a patient's condition worsens.

For example, a Digital Medical Twin is a virtual replica of a patient updated constantly with sensor and health record data. This requires ultra-reliable, low-latency communication (Rajab, 2024). Doctors can simulate treatments on the twin without risking the patient. Hospitals can also model equipment failures to schedule maintenance.

In a 6G-enabled hospital, several operations happen at once:
- Sensors on patients transmit vital signs frequently. AI flags anomalies and alerts staff before visible deterioration.
- A remote specialist guides a local team using a robotic system over 6G, with no noticeable delay.
- Connected medication dispensers and equipment trackers coordinate to prevent stock-outs.
- Digital models of ward occupancy help staff manage beds and patient flow.

These connections introduce risk. A single compromised device could affect multiple systems, making security a primary design requirement.

3. WEARABLE DEVICES AND IOMT IN HEALTHCARE
3.1 Types and functions of wearables
The IoMT includes consumer fitness bands, hospital monitors, and implanted biosensors (Figure 8.1).

Major categories include:
- Consumer wearables like smartwatches and trackers that monitor heart rate, sleep, and oxygen levels.
- Medical-grade wearables like glucose monitors, ECG patches, and blood pressure cuffs that provide precision for medical decisions.
- Implantable sensors such as cardiac defibrillators and cochlear implants that offer internal access that external devices cannot.
- Smart clinical equipment like hospital beds with movement sensors, connected infusion pumps, and modern ventilators.

These devices all collect physiological data automatically. They track heart rate, blood pressure, oxygen, temperature, glucose, and activity (S. S. Al-Mekhlafi et al., 2025c). AI systems use this data for monitoring and diagnostics.

3.2 Monitoring, real-time feedback, and data analytics
IoMT monitors patients constantly, unlike periodic clinic visits. This continuous tracking reveals subtle trends like a shifting resting heart rate or changing gait that isolated checks miss (S. S. Al-Mekhlafi et al., 2025c).

AI analyzes this data in a few specific ways:
- It identifies signs of early sepsis, arrhythmia, or low blood sugar before symptoms appear. Early intervention usually leads to better outcomes and lower costs.
- It uses a patient's specific data history to suggest tailored interventions. In physical therapy, adapting exercises based on live data improves recovery.
- It summarizes patient data for clinicians, helping them make fast decisions without digging through records (S. S. Al-Mekhlafi et al., 2025c).
- It analyzes medical images, genomic data, and behavioral sensors to build a complete picture of patient health (A. Al-Mekhlafi et al., 2023).

3.3 Benefits and constraints
IoMT deployment has clear benefits but faces several constraints. Table 8.2 outlines these.

Table 8.2: Key Features, Benefits, and Constraints of Wearable Devices and IoMT
| Key Features | Benefits | Constraints |
|--------------|----------|-------------|
| Continuous health monitoring, remote patient monitoring, AI-driven analytics | Fewer hospital visits, earlier disease detection, improved clinical communication (S. S. Al-Mekhlafi et al., 2025c) | Data security risks, interoperability gaps, AI bias, battery life limits (S. S. Al-Mekhlafi et al., 2025c) |

Patients with chronic conditions can be monitored at home, saving travel time and costs. Clinicians get more complete data histories. Home monitoring also helps patients in remote areas or with limited mobility access specialists (S. S. Al-Mekhlafi et al., 2025c).

However, continuous data collection increases privacy risks. Opaque AI models, whose logic is unclear to doctors, raise concerns about accountability (S. S. Al-Mekhlafi et al., 2025c). Technical issues like short battery life and the difficulty of connecting different devices to hospital systems also slow down adoption.

4. INTEGRATION MODELS AND IMPLEMENTATION FRAMEWORKS
4.1 Proposed architecture for 6G-IoMT integration
Integrating IoMT devices with 6G requires a layered architecture. Each level performs specific functions while communicating with the levels above and below it.

The five layers function as follows:
- Device Layer: This includes implantable sensors, IoT medical devices, and wearable sensors. These devices generate the raw physiological data streams (A. Al-Mekhlafi et al., 2025b).
- Communication Layer: This layer provides the 6G wireless connection. It uses IoT protocols and secure transmission to move data quickly, ensuring the ultra-low latency needed for medical apps.
- Edge / Fog Layer: Local data analytics and edge AI processing happen here. This layer handles time-sensitive computations physically close to the user to ensure immediate response.
- Cloud Intelligence Layer: This layer manages massive storage and heavy processing. It handles big data analytics, AI model training, and maintains digital health twins.
- Application Layer: This translates processed data into clinical services, like predictive healthcare, telemedicine, and remote patient monitoring (A. Al-Mekhlafi et al., 2025b).

Future versions of this architecture will include AI-native networks that manage routing, multi-access edge computing (MEC) that distributes processing, and ISAC capabilities (Rajab, 2024). Figure 8.2 illustrates this more responsive healthcare ecosystem.

4.2 Data flow, edge/cloud coordination, and device communication
Understanding how data moves through this architecture clarifies its capabilities and vulnerabilities (Figure 8.3).

Data flow
Sensors send continuous data on physiological signs and activity. This data passes through encrypted links to edge nodes for quick processing, or to cloud platforms for slower, complex analysis. This ensures data is processed based on urgency: emergency alerts are analyzed locally within milliseconds, while long-term trend analysis happens in the cloud (S. S. Al-Mekhlafi et al., 2025c).

Edge/cloud coordination
Edge computing lets AI inference run locally inside the hospital. This means patient data does not have to leave the secure network, reducing interception risks. Models can be trained locally using federated learning, limiting central data storage (A. Al-Mekhlafi et al., 2025d). Cloud platforms still handle tasks like training large deep learning models, storing long-term records, and tracking population health.

Device communication protocols
Current IoMT uses different wireless protocols, like 5G for fast apps and NB-IoT for low-power monitors. 6G will simplify this by offering enough bandwidth in the terahertz band to handle different protocols on one network (VDE, 2024). Developers are also creating healthcare-specific protocols to stop data from being trapped in proprietary, incompatible formats.

4.3 Implementation and scalability challenges
Moving from this architectural vision to wide clinical deployment presents several challenges.

- Infrastructure upgrades: 6G requires dense small-cell antenna networks and upgrades to old medical devices. Most health systems do not have the budget for this.
- High costs: The total cost of 6G infrastructure, new IoMT devices, and system integration is high, especially for providers in lower-income areas.
- Data management complexity: A fully equipped 6G-IoMT hospital generates huge amounts of data. Processing mixed data types—sensor readings, clinical notes, and large images—is computationally difficult.
- Interoperability and standardization: Without universal communication standards, data from one vendor’s device often cannot be used by another vendor’s analytics platform without expensive custom integration (S. S. Al-Mekhlafi et al., 2025c).
- Scalability: As more devices and patients connect, the system must maintain performance and security. Architectures that work for thousands of devices may fail with millions (DelveInsight, 2025).

5. CASE STUDIES AND USE CASES IN DIAGNOSTICS
The integration of 6G, IoMT, and AI produces concrete clinical results, shown in recent pilot programs.

5.1 Remote patient monitoring (RPM)
AI-driven RPM lets doctors oversee chronic conditions by analyzing real-time wearable data to generate personalized alerts (S. S. Al-Mekhlafi et al., 2025c).

Case Study 1: Diabetes management
A study paired continuous glucose monitors with a machine learning engine that learned a patient's glycemic patterns. The engine provided customized dietary, medication, and alert recommendations. Over six months, participants reduced their HbA1c levels by 20%. Patients followed the AI's advice more closely because the feedback was immediate and personalized, unlike traditional delayed guidance.

Case Study 2: Post-surgical monitoring
After cardiac surgery, a program monitored patients' vital signs, including heart rate and blood pressure, triggering alerts if readings strayed from their personal baselines. The system flagged early complications like arrhythmias and wound infections, which helped reduce hospital readmissions by 30%. Avoiding readmissions after cardiac surgery saves money and reduces mortality risk.

Case Study 3: Elderly care monitoring
An elderly care program combined vital sign monitoring with fall detection and physical decline tracking. Constant surveillance let clinicians intervene before minor issues became emergencies, improving outcomes for this vulnerable group.

These cases show a shift from passive observation to predictive, active intervention.

5.2 Individualized AI treatments
Fast 6G connectivity allows AI to process imaging, genomic, and sensor data at the same time to guide medical treatment (S. S. Al-Mekhlafi et al., 2025b).

Key clinical applications include:
- Early sepsis prediction: Models can identify at-risk patients hours before visible signs appear. Administering antibiotics during this window improves survival rates.
- Oncology and cardiovascular risk: AI algorithms analyze imaging and genomic data in real time to provide diagnostic feedback and detect cancer and heart disorders early (A. Al-Mekhlafi et al., 2025c).
- Adaptive rehabilitation: In physical therapy, AI adjusts exercise intensity and frequency based on real-time data, leading to faster recovery and better patient compliance.

5.3 Telemedicine
The telemedicine use case for 6G is highly consequential for geographic equity. Ultra-fast, low-latency connectivity enables consultations that are clinically rigorous, not just conversational.

- Remote surgery (Telesurgery): Connecting a robotic surgical platform to a 6G network removes perceptible delay between a surgeon’s input and the robot’s movement. Surgeons can guide or perform operations from far away, bringing specialized skills to rural hospitals (A. Al-Mekhlafi et al., 2025). AI embedded in the robot provides haptic feedback and procedural warnings.
- Immersive consultations: Extended reality platforms let clinicians and patients interact in 3D environments. Doctors can use holographic visualization for pre-operative planning, and patients can use virtual reality for pain management (MedicalExpo, 2024).

5.4 Solutions to sustainability, data burden, and ethics
- Sustainability: 6G network design includes energy efficiency targets to meet environmental goals (Kaur & Gupta, 2025a). Researchers are testing ways to power low-energy IoMT devices by harvesting ambient thermal or kinetic energy.
- Data burden: AI systems handle large data volumes by doing the initial analysis, only flagging important patterns for clinicians. Blockchain-based ledgers track who accesses this data without centralizing sensitive information (H. K. S. A. Al-Mekhlafi et al., 2023).
- Ethics: Healthcare AI needs rules that include ethical principles from the start. Informed consent, clear algorithms, and equal access must be design requirements, not just compliance steps added later (Lekadir et al., 2025).

5.5 Real-world exemplars
While full 6G commercial use is years away, research prototypes prove clinical feasibility.

- Google’s prenatal monitoring initiative: This program tests AI-driven sensors on a 6G network to monitor fetal and maternal health, showing that real-time data fusion is possible.
- Guangzhou physiotherapy system: A physical therapy application on Guangzhou’s 6G infrastructure adjusts treatment parameters in real time, proving that adaptive AI therapy works in clinical workflows.

6. SECURITY, PRIVACY, AND ETHICAL CONSIDERATIONS
The expanded connectivity surface of 6G introduces new security risks that require new defenses.

6.1 Health data risks and security strategies
Each distinctive capability of 6G corresponds to a distinctive security exposure (Table 8.4). The five primary threat categories are:

1. Immersive communication vulnerabilities: Remote surgical sessions carry high interception risk. An attacker disrupting a telesurgery data stream could alter instrument control signals or vital signs, potentially causing harm (A. Al-Mekhlafi et al., 2025a). Protecting these channels requires end-to-end encryption and integrity verification.
2. HRLLC attacks: The microsecond latency that makes 6G useful for remote surgery also creates a weakness. Denial of Service (DoS) attacks can slow communication mid-operation, degrading quality below clinical standards (A. Al-Mekhlafi et al., 2025a).
3. Massive connectivity as attack surface: 6G supports billions of active devices, meaning any unsecured device is a network entry point. A compromised bedside monitor could allow attackers to access health records, manipulate configurations, or disrupt hospital operations (A. Al-Mekhlafi et al., 2025a).
4. Ubiquitous connectivity spreading breaches: When coverage spans hospitals, ambulances, and home care, a breach in one node can spread rapidly (A. Al-Mekhlafi et al., 2025a). Network segmentation and anomaly detection are critical defenses.
5. AI model vulnerabilities: The AI diagnostic systems are attack targets themselves. Model poisoning attacks, where bad data is inserted during training, corrupt predictions in ways standard monitoring cannot detect (A. Al-Mekhlafi et al., 2025a). The clinical risk of misdiagnosis requires dedicated research.

These threats show that security in 6G cannot be an afterthought; developers must build it into every layer, from the physical radio interface to application logic (A. A. Al-Mekhlafi et al., 2024).

Table 8.4: Security Challenges in 6G-IoMT Healthcare and XAI Mitigation Strategies
| Challenge Category | Specific Security Implication | XAI Mitigation Strategy |
|--------------------|-------------------------------|-------------------------|
| Immersive Comm. | Interception/alteration of patient data; DoS attacks | Transparency to reveal data manipulation |
| HRLLC | Latency attacks delaying critical procedures | Real-time anomaly detection |
| Massive Comm. | Unsecured devices as network entry points | Identifying compromised devices |
| Ubiquitous Conn. | Rapid breach propagation | Cross-validation for threat detection |
| AI Integration | Model/data poisoning causing misdiagnoses | Explainability (SHAP, LIME) to understand AI decisions |
| ISAC | Compromised sensors injecting false data | Interpreting sensor anomalies |

6.2 Real-time data transmission safeguards
Protecting transmitted health data involves four properties:

1. Confidentiality: Health information must remain inaccessible to unauthorized parties. End-to-end encryption using algorithms resilient against future computation, like post-quantum cryptography, provides this security (A. Al-Mekhlafi et al., 2025c).
2. Integrity: Attackers who cannot decrypt data might still try to corrupt it. Changing vital signs or imaging data causes diagnostic errors. Cryptographic hashes and digital signatures verify data integrity.
3. Availability: Clinical systems need continuous service. DoS attacks on communication infrastructure delay critical alerts. Redundant pathways and failover mechanisms ensure availability.
4. Authenticity and anonymity: Both communicating parties must verify their identities to prevent unauthorized devices from injecting data. Anonymization techniques decouple patient attributes from transmitted health parameters to protect privacy on shared networks (A. Al-Mekhlafi et al., 2025c).

6.3 Compliance and ethical AI design
Regulatory compliance
The regulations governing health data processing are strict and vary by location. In the US, HIPAA sets standards for protecting patient information. In the EU, GDPR imposes stringent requirements and penalties (A. Al-Mekhlafi et al., 2025c). Healthcare organizations deploying 6G-IoMT across borders must follow both, requiring coordinated legal and technical effort (Kaur & Gupta, 2025b).

Ethical AI design: The FUTURE-AI framework
The FUTURE-AI framework identifies six guiding principles for ethical AI development in healthcare (Lekadir et al., 2025). Table 8.3 outlines these principles.

Table 8.3: Ethical Principles and Compliance Frameworks for AI in Healthcare
| Principle | Description | Relevant Regulation |
|-----------|-------------|---------------------|
| Fairness | Maintain consistent performance across diverse populations | FUTURE-AI; WHO; OECD |
| Universality | Function predictably across diverse settings | FUTURE-AI |
| Traceability | Ensure accountability and auditability of AI decisions | FUTURE-AI |
| Usability | Integrate effectively into clinical workflows | FUTURE-AI |
| Robustness | Remain reliable and accurate under varying conditions | FUTURE-AI |
| Explainability| Provide clinically meaningful accounts of decision logic | FUTURE-AI |
| Patient Autonomy | Enhance patient choices and ensure informed consent | HIPAA; GDPR |
| Human Oversight | Augment, not replace, healthcare professionals | WHO Guidelines |

Three principles directly affect operations:
1. Fairness and bias mitigation: Training datasets that lack demographic diversity produce biased diagnostic models. Developers must curate broad training data and use fairness-aware learning (Kaur & Gupta, 2025b).
2. Transparency and explainability (XAI): Clinicians cannot oversee recommendations they do not understand. Opaque AI systems erode trust and impede adoption (Kaur & Gupta, 2025b). Techniques like SHAP and LIME produce human-interpretable accounts of AI reasoning (A. Al-Mekhlafi et al., 2025e).
3. Accountability and human oversight: When AI contributes to a misdiagnosis, legal responsibility is often unclear. Frameworks must specify accountability and preserve human oversight before scaling AI in clinical care (Lekadir et al., 2025).

7. CHALLENGES AND FUTURE DIRECTIONS
Several obstacles prevent full clinical deployment of 6G-IoMT at population scale.

7.1 Technical bottlenecks
1. Power consumption: Sustaining connections for billions of medical sensors uses significant energy. Battery-powered wearables face a trade-off between transmission strength and lifespan. Researchers are investigating energy harvesting from ambient sources (MedicalExpo, 2024).
2. Spectrum utilization: 6G will use frequencies up to 100 GHz and the terahertz band. Allocating this spectrum requires slow regulatory processes, national coordination, and interference management. Proactive regulatory engagement is necessary before commercial deployment (DelveInsight, 2025).
3. Interoperability: Health informatics already struggles with incompatible data formats. With millions of connected devices, this fragmentation causes more problems (S. S. Al-Mekhlafi et al., 2025c). Universal communication standards are required for a unified IoMT ecosystem.
4. Data scarcity for AI training: AI models require massive amounts of labeled training data. This data is often missing or trapped behind institutional walls for privacy or competitive reasons (Kaur & Gupta, 2025b).

7.2 Research trends
Research is advancing across several areas:
1. Novel sensors: Wearable sensors are becoming smaller, more energy-efficient, and capable of monitoring breathing rates, sweat, and tear electrolytes (S. S. Al-Mekhlafi et al., 2025a). Radar-based, contactless sensing allows monitoring for patients who cannot tolerate wearables.
2. Federated AI (Federated learning): Federated Learning (FL) addresses the tension between needing large datasets and protecting privacy. FL distributes training across hospitals or devices. Each node trains locally and contributes only parameter updates to the central model, keeping patient data at the source (A. Al-Mekhlafi et al., 2025d).
3. Edge computing optimization: Researchers are optimizing edge computing for latency and power consumption by managing tasks dynamically between edge and cloud servers (DelveInsight, 2025).
4. Digital twins: Virtual replicas of physical entities, integrating genomic, physiological, and behavioral data, provide simulation environments for treatment planning (Rajab, 2024).
5. Explainable AI (XAI): Healthcare XAI research is moving toward models that are transparent by design, which improves clinical adoption and hardens the systems against manipulation (A. Al-Mekhlafi et al., 2025e).

These areas overlap. Federated learning addresses data scarcity and privacy. Edge computing reduces latency and confines sensitive data. XAI strengthens security and supports ethical transparency.

7.3 Strategic policy and cross-disciplinary collaboration
1. Strategic policy: The regulations for 6G spectrum allocation, security standards, and device certification are being written now. Healthcare needs specific rules regarding reliability, security, and privacy built into these frameworks.
2. Cross-disciplinary collaboration: Developing 6G healthcare systems requires engineering, clinical, regulatory, and social science expertise. Programs like Europe’s Hexa-X and the US Next G Alliance organize this effort at scale.
3. Equitable access: The benefits of 6G-IoMT could bypass low-income systems unless developers design for affordability. Funding must distribute infrastructure costs, and procurement must prioritize open standards.

8. CONCLUSION
The convergence of 6G wireless networks, IoMT devices, and AI-driven analytics changes healthcare from episodic management to continuous, anticipatory care.

6G’s core properties—sub-microsecond latency, terabit-per-second throughput, AI-native networks, and ubiquitous coverage—provide the technical foundation. IoMT devices gather the data, and AI systems extract actionable insight. Together, they create capabilities that exceed what any single component offers.

However, realizing this potential requires addressing institutional and regulatory challenges:
1. Security by design: Security architecture must be embedded at every layer to counter HRLLC attacks, model poisoning, and breach propagation.
2. Universal interoperability standards: A unified IoMT architecture requires enforced interoperability standards.
3. Ethical AI governance: Fairness, transparency, and human oversight must be design constraints, implemented through XAI and federated learning.
4. Equitable distribution: Technical feasibility does not guarantee equitable access. Policymakers must make deliberate choices to ensure broad distribution.

When developers and policymakers meet these conditions, the 6G-IoMT healthcare revolution can become a practical and equitable reality. The decisions made in the next decade will determine the outcome.

References
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Hagri, M. A. (2024). “The fusion of IoMT with cloud and edge computing offers a promising path forward, combining centralised processing power with localised, real-time analytics.” Int. J. Precis. Remote Sens., vol. 4, no. 12, pp. 119–128.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Hagri, M. A. (2025). Leveraging IoT for Smart Healthcare: Enhancing Remote Patient Monitoring, Disease Prediction, and Real-Time Decision-Making through AI-Driven Analytics. Research Gate.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2020). “IoT as a new paradigm with a significant role in healthcare.” Pearl.
Al-Mekhlafi, A., et al. (2022). “Security and privacy reconsideration in next-generation wireless environments.” Int. J. Environ. Res. Public Health, 8.
Al-Mekhlafi, A., et al. (2023). Next-generation wireless communication: Innovations, challenges, and the convergence of AI, IoT, and 6G. Research Gate.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023a). “Analysis of integration of IoMT with blockchain issues, challenges and solutions.” Research Gate.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023b). “IoMT technologies enable medical devices to transmit data to medical practitioners, who can monitor a patient’s condition without reading the bedside records.” Sci. Adv. Netw. Data Sci., vol. 1, no. 1, p. 8.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023c). “Data security and privacy compliance in 5G and 6G healthcare networks.” Front. Public Health, vol. 11, p. 10719543.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023d). “The Internet of Things has brought a revolutionary change in the healthcare system.” Research Gate.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023e). “The 6G network: the next major game-changer in the telecom industry.” Sensors, vol. 10, no. 7, p. 347022.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2023f). “6G mobile technology in various application fields.” Sensors, 10.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024a). “Security and privacy of transmitted data in advancing IoMT systems.” Sensors, vol. 11, no. 9, p. 86172.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024b). “The development of 6G technology is driving telemedicine, facilitating remote consultations, diagnosis, and treatment.” IGI Global.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024c). “Exceptional Speed: Enables data transmission rates reaching 1 terabit per second.” Research Gate.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024d). “The vision for 6G: faster data rates, near-zero latency, and higher capacity for an AI-driven digital ecosystem.” arXiv preprint arXiv:2410.21986v1.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024e). “The integration of artificial intelligence (AI) and sixth generation (6G) communication networks has emerged as a transformative paradigm.” arXiv preprint arXiv:2412.14538v3.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024f). The integration of healthcare with IoT, driven by AI and supported by cloud computing.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2024g). “New architectural concepts supporting the 6G vision.” Future Internet, 6.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025a). “The worldwide IoMT market is predicted to reach over $200 billion by 2030.” J. Emerg. Technol. Innov. Res., vol. 11, no. 1, pp. 113–120.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025b). “Federated learning in healthcare: prevalent types, uses, issues, and future research directions.” Open Neuroimaging J., vol. 18, no. 1, pp. 353032–353032.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025c). “Recent advances in AI-driven wireless communication are driving the adoption of 6G technologies in hospital environments.” Sensors, vol. 25, no. 11, p. 3280.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025d). “AI algorithms in healthcare analysing high-resolution imaging and genomic data in real time for early disease detection.” arXiv preprint arXiv:2506.10570v1.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025e). “Security and privacy in 6G networks: challenges and potential solutions.” SciSpace.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025f). “Improving RPM through AI for patient-centric healthcare delivery.” Future Internet, 70.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025g). “6G networks for complicated medical services: ultra-high-speed communication, minimal latency, and massive interconnectedness.” Artif. Intell. Innov. Technol. J, 3, pp. 24–30.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025h). “Smart healthcare integrating traditional medical services, advanced IT infrastructure, and big data analysis.” J. Commun, 20.
Al-Mekhlafi, A., Al-Mekhlafi, S. A., Al-Mekhlafi, S. S., & Al-Mekhlafi, A. A. (2025i). The impact of AI in clinical diagnostics, COVID-19 early diagnosis, virtual patient care, and electronic health records. Research Gate.
Al-Mekhlafi, S. S., Al-Hagri, M. A., Al-Mekhlafi, S. A., & Al-Mekhlafi, A. A. (2025a). “In the context of smart hospitals, the infusion of 6G facilitates real-time communication among a myriad of medical devices, sensors, and systems...” Research Gate.
Al-Mekhlafi, S. S., Al-Hagri, M. A., Al-Mekhlafi, S. A., & Al-Mekhlafi, A. A. (2025b). AI for diagnostics in healthcare. Research Gate.
Alwakeel, A. M. (2025). “Synergistic Integration of Edge Computing and 6G Networks for Real-Time IoT Applications.” Mathematics, vol. 13, no. 9, p. 1540. doi: 10.3390/math13091540.
Chataut, R., Nankya, M., & Akl, R. (2024). “6G Networks and the AI Revolution: Exploring Technologies, Applications, and Emerging Challenges.” Sensors, vol. 24, no. 6, p. 1888. doi: 10.3390/s24061888.
DelveInsight. (2025). How AI-Driven Diagnostics Are Transforming Healthcare Delivery.
Digital Regulation Platform. (2025). “Overview of 6G (IMT-2030).” Digital Regulation Platform.
Garg, P., & Singh, A. K. (2025). “From Data to Diagnosis: Unleashing AI and 6G in Modern Medicine.” Research Gate.
GreyB. (2024). “6G Technology Impact Areas.” GreyB.
International Bar Association. (2023). “AI in healthcare: legal and ethical considerations.” Int. Bar Assoc.
Kaur, N., & Gupta, L. (2025a). “Explainable AI for Securing Healthcare in IoT-Integrated 6G Wireless Networks.” arXiv preprint arXiv:2505.14659.
Kaur, N., & Gupta, L. (2025b). “Explainable AI Assisted IoMT Security in Future 6G Networks.” Future Internet, 17(5). doi: 10.3390/fi17050226.
Keysight. (2025). “Keysight’s 6G Research Collaborations Accelerate the Future of Wireless.” GA Institute.
Kumar, A., Masud, M., Alsharif, M. H., Gaur, N., & Nanthaamornphong, A. (2025). “Integrating 6G technology in smart hospitals: challenges and opportunities for enhanced healthcare services.” Front. Med. (Lausanne), 12, 1534551. doi: 10.3389/fmed.2025.1534551.
Lekadir, K., Frangi, A. F., Porras, A. R., Glocker, B., et al. (FUTURE-AI Consortium). (2025). “FUTURE-AI: international consensus guideline for trustworthy and deployable artificial intelligence in healthcare.” BMJ, vol. 388, p. e081554. doi: 10.1136/bmj-2024-081554.
Mabina, A., Rafifing, N., Seropola, B., Monageng, T., & Majoo, P. (2024). “Challenges in IoMT Adoption in Healthcare: Focus on Ethics.” Eur. Conf. Cyber Warf. Secur., vol. 23, no. 1, pp. 586–594.
Masoumian Hosseini, M., Masoumian Hosseini, S. T., Haghighi, E., et al. (2025). “The revolutionary impact of 6G technology on empowering health and building a smart society: A scoping review.” Comput. Biol. Med., 194, 110496. doi: 10.1016/j.compbiomed.2025.110496.
MedicalExpo. (2024). “6G in healthcare: next-generation connectivity.” MedicalExpo.
Nigar, N. (2024). “AI in Remote Patient Monitoring.” arXiv preprint arXiv:2407.17494.
Pham, T. (2025). “Ethical and legal considerations in healthcare AI: innovation and policy for safe and fair use.” R. Soc. Open Sci., vol. 12, no. 5, p. 241873. doi: 10.1098/rsos.241873.
Rajab, R. M. (2024a). “Communication Protocols for Internet of Medical Things (IoMT).” Research Gate.
Rajab, R. M. (2024b). The advent of sixth-generation (6G) technology: revolutionary transformation in healthcare.
Supermicro. (2024). 6G Research.
VDE. (2024). “6G networks in medicine and medical technology.” VDE.
Vinnova. (2024). “6G – international research and innovation collaboration 2025.” Vinnova.
