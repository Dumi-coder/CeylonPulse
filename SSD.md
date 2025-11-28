# Signal Specification Document

##   POLITICAL SIGNALS (P)

**These reflect governmental, regulatory, and political stability factors.**

### 1. Government Policy Announcements

-  Why: Direct impact on tax, imports, exports, businesses

- Signal Specification DocumentSource: News, Ministry Website

-  Detect: Keyword spikes (“policy”, “tax”, “cabinet approves”, “budget”)

-  PESTLE: P

-  Output: National Activity

-  Frequency: Every 1 hour

-  Priority: HIGH

### 2. Cabinet/Parliament Decisions

-  Why: Policy change → affects business operations

-  Detection: Topic modeling + keyword detection

-  PESTLE: P

-  Output: National Activity

-  Priority: HIGH

### 3. Government Sector Strike Warnings

-  Why: Direct operational disruption

-  Source: News, Union FB/Twitter

-  PESTLE: P

-  Output: Operational Risk

-  Priority: HIGH

### 4. Police/Security Alerts

-  Why: Impacts safety, movement

-  PESTLE: P

-  Output: Risk

-  Priority: HIGH

### 5. Election-related Discussions

-  Why: Predicts instability

-  PESTLE: P

- Priority: MEDIUM

6. Foreign Policy / International Agreements

-  Why: Imports/exports, tourism

-  PESTLE: P

-  Priority: MEDIUM

7. Tax Revision Rumors

-  Why: Direct economic impact

-  PESTLE: P

-  Priority: HIGH

8. Public Protests & Demonstrations

-  Why: Traffic, business closures

-  PESTLE: P

-  Priority: HIGH

##   ECONOMIC SIGNALS (E)
9. Inflation Mentions

-  Why: Consumer spending power

-  Source: News + Twitter

-  Detect: Keyword trends

-  Output: Economic Indicator

-  Priority: HIGH

10. Fuel Shortage Mentions

-  Why: Logistics, mobility

-  Output: Operational Risk

-  Priority: HIGH

11. Dollar Rate Discussions

-  Why: Imports, cost

-  Detect: Frequency spikes

-  Priority: HIGH

12. Tourism Search Trend (Google Trends)

-  Why: Hotel/retail opportunity

-  Output: Opportunity

-  Priority: HIGH

13. Food Price Spikes

-  Why: Retail & consumer stress

-  Source: News

-  Priority: MEDIUM

14. Stock Market Volatility

-  Why: Business investor confidence

-  Priority: MEDIUM

15. Foreign Investment News

-  Why: Sector opportunities

-  Priority: LOW

16. Currency Black Market Mentions

-  Why: Informal economy changes

-  Priority: MEDIUM

##   SOCIAL SIGNALS (S)
17. Crime & Safety Alerts

-  Why: Travel & movement risks

-  Source: News

-  Priority: HIGH

18. Public Sentiment (Social Media)

-  Why: Demand, reactions

-  Sentiment model

-  Priority: HIGH

19. Migration / Visa Interest

-  Why: Brain drain → labor availability

-  Source: Google Trends

-  Priority: MEDIUM

20. Public Health Discussions

-  Why: Disease outbreaks affect business

-  Priority: HIGH

21. Viral Social Trends

-  Why: Consumer behavior

-  Priority: MEDIUM

22. Cultural Event Mentions

-  Why: Retail & tourism impacts

-  Priority: LOW

## TECHNOLOGICAL SIGNALS (T)
23. Power Outages (CEB)

-  Why: Direct business disruption

-  Priority: HIGH

24. Telecom Outages

-  Why: Internet downtime impacts all businesses

-  Source: Users + social media

-  Priority: HIGH

25. Cyberattack Mentions

-  Why: Security risk

-  Priority: MEDIUM

26. E-commerce Growth Indicators

-  Why: Market opportunity

-  Priority: LOW

27. Digital Payments Failure Reports

-  Why: Retail operations

-  Priority: HIGH

## LEGAL SIGNALS (L)
28. New Regulations Affecting Businesses

-  Why: Compliance

-  Priority: HIGH

29. Court Rulings Impacting Industries

-  Why: Legal operational shifts

-  Priority: MEDIUM

30. Import/Export Restriction Changes

-  Why: Supply chain effects

-  Priority: HIGH

31. Customs/Port Delays

-  Why: Logistics

-  Priority: MEDIUM

##  ENVIRONMENTAL SIGNALS (E)
32. Rainfall Alerts

-  Why: Delivery + flooding

-  Priority: HIGH

33. Flood Warnings

-  Why: Heavy business disruption

-  Priority: HIGH

34. Heat Wave Alerts

-  Why: Tourism + energy usage

-  Priority: MEDIUM

35. Landslide Warnings

-  Why: Major logistics risk

-  Priority: HIGH

36. Cyclone Updates

-  Why: Severe disruptions

-  Priority: HIGH

37. Air Quality Index Changes

-  Why: Health & public movement

-  Priority: MEDIUM

38. Drought Warnings

-  Why: Agriculture & water supply

-  Priority: MEDIUM

39. Water Supply Cuts (NWSDB)

-  Why: Businesses & households impacted

-  Priority: HIGH

40. Coastal Erosion / Tsunami Alerts

-  Why: Tourism, fisheries

-  Priority: LOW

## 📌 SUMMARY TABLE (PESTLE Distribution)

-  Category	Signals Count
-  Political	8
-  Economic	8
-  Social	6
-  Technological	5
-  Legal	4
-  Environmental	9
-  TOTAL	40
