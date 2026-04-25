"""
Management command to seed the database with 10 realistic developer profiles.
Usage: python manage.py seed_developers
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_save
from users.models import Profile, Skill
from users.signals import create_profile
from projects.models import Project, Tag


DEVELOPERS = [
    {
        "username": "emmawilson",
        "first_name": "Emma",
        "last_name": "Wilson",
        "email": "emma.wilson@protonmail.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Emma Wilson",
            "location": "San Francisco, CA",
            "short_intro": "Senior Full-Stack Engineer at Stripe | Open Source Enthusiast",
            "bio": (
                "I'm a full-stack engineer with 7+ years of experience building scalable "
                "payment infrastructure and developer tools. Currently at Stripe, where I "
                "work on the Payments API team. Previously built internal tooling at Shopify. "
                "I'm passionate about clean architecture, developer experience, and making "
                "complex systems feel simple. When I'm not coding, you'll find me contributing "
                "to Django REST Framework or mentoring at local bootcamps."
            ),
            "social_github": "https://github.com/emmawilson",
            "social_twitter": "https://twitter.com/emmawilsondev",
            "social_linkedin": "https://linkedin.com/in/emmawilson",
            "social_website": "https://emmawilson.dev",
        },
        "skills": [
            {"name": "Python", "description": "7+ years building backend services, APIs, and data pipelines with Python. Expert in Django, Flask, and FastAPI."},
            {"name": "Django", "description": "Core contributor to several Django packages. Built production apps serving millions of requests daily."},
            {"name": "TypeScript", "description": "Strongly-typed frontend and Node.js backend development. Extensive experience with complex type systems."},
            {"name": "React", "description": "Built component libraries and complex SPAs. Proficient with hooks, context, and state management."},
            {"name": "PostgreSQL", "description": "Database design, query optimization, and performance tuning for high-traffic applications."},
            {"name": "Docker", "description": "Containerization of microservices, multi-stage builds, and Docker Compose for local development."},
            {"name": "AWS", "description": "EC2, Lambda, S3, RDS, CloudFront — full cloud infrastructure management and deployment."},
        ],
        "projects": [
            {
                "title": "PayFlow SDK",
                "description": "An open-source Python SDK for integrating multiple payment gateways (Stripe, PayPal, Square) through a unified API. Features automatic retry logic, webhook handling, and comprehensive test coverage.",
                "tags": ["django", "docker"],
                "vote_total": 87,
                "vote_ratio": 94,
                "source_link": "https://github.com/emmawilson/payflow-sdk",
                "demo_link": "https://payflow-sdk.readthedocs.io",
            },
            {
                "title": "DevDash",
                "description": "A real-time developer dashboard built with React and Django that aggregates GitHub activity, CI/CD status, and deployment metrics into a single view. Used internally by a 50-person engineering team.",
                "tags": ["react", "django", "docker"],
                "vote_total": 64,
                "vote_ratio": 88,
                "source_link": "https://github.com/emmawilson/devdash",
            },
        ],
    },
    {
        "username": "marcosrivera",
        "first_name": "Marcos",
        "last_name": "Rivera",
        "email": "marcos.rivera@hey.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Marcos Rivera",
            "location": "Austin, TX",
            "short_intro": "Backend Engineer @ Vercel | Rust & Go | Systems Programming",
            "bio": (
                "Systems-level thinker with a product-minded approach. I spend my days "
                "building high-performance edge infrastructure at Vercel and my evenings "
                "exploring Rust and WebAssembly. Before tech, I studied mechanical engineering "
                "at UT Austin, which gave me a deep appreciation for efficiency and precision. "
                "I believe the best code is code that doesn't need to exist — simplicity is "
                "the ultimate sophistication. Currently exploring how WASM can bridge the gap "
                "between native and web performance."
            ),
            "social_github": "https://github.com/marcosrivera",
            "social_twitter": "https://twitter.com/marcosdev",
            "social_linkedin": "https://linkedin.com/in/marcos-rivera-dev",
        },
        "skills": [
            {"name": "Go", "description": "Built production microservices handling 100K+ requests/sec. Expertise in concurrency patterns and gRPC."},
            {"name": "Rust", "description": "Systems programming, CLI tools, and WASM modules. Active Rust community contributor."},
            {"name": "Python", "description": "Scripting, automation, and backend development. Built data processing pipelines with asyncio."},
            {"name": "Docker", "description": "Container orchestration, multi-stage builds, and production-grade Dockerfiles."},
            {"name": "Kubernetes", "description": "Cluster management, Helm charts, and auto-scaling configurations for production workloads."},
            {"name": "GraphQL", "description": "Designed and maintained GraphQL APIs serving multiple frontend clients simultaneously."},
        ],
        "projects": [
            {
                "title": "EdgeCache",
                "description": "A high-performance edge caching layer written in Rust that reduces API latency by up to 70%. Supports LRU, LFU, and TTL-based eviction strategies with a simple configuration API.",
                "tags": ["docker"],
                "vote_total": 112,
                "vote_ratio": 96,
                "source_link": "https://github.com/marcosrivera/edgecache",
            },
            {
                "title": "GoMQ",
                "description": "A lightweight message queue implementation in Go designed for microservice communication. Features persistent storage, dead-letter queues, and at-least-once delivery guarantees.",
                "tags": ["docker", "graphQL"],
                "vote_total": 73,
                "vote_ratio": 91,
                "source_link": "https://github.com/marcosrivera/gomq",
                "demo_link": "https://gomq.dev/docs",
            },
        ],
    },
    {
        "username": "priyasharma",
        "first_name": "Priya",
        "last_name": "Sharma",
        "email": "priya.sharma@gmail.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Priya Sharma",
            "location": "London, UK",
            "short_intro": "ML Engineer @ DeepMind | NLP & Computer Vision | PhD in AI",
            "bio": (
                "Machine learning engineer with a PhD in Artificial Intelligence from Imperial "
                "College London. My research focused on multi-modal transformers for medical image "
                "analysis. At DeepMind, I work on large language model alignment and safety. "
                "I'm deeply passionate about making AI accessible and responsible. I regularly "
                "speak at conferences like NeurIPS and ICML, and maintain several popular open-source "
                "ML libraries. Strong advocate for diversity in STEM — I mentor women in AI through "
                "the Women in Machine Learning community."
            ),
            "social_github": "https://github.com/priyasharma-ml",
            "social_twitter": "https://twitter.com/priyasharma_ai",
            "social_linkedin": "https://linkedin.com/in/priya-sharma-ml",
            "social_website": "https://priyasharma.ai",
        },
        "skills": [
            {"name": "Python", "description": "Primary language for ML research and production systems. Expert in scientific Python ecosystem."},
            {"name": "PyTorch", "description": "Built and trained transformer models, custom loss functions, and distributed training pipelines."},
            {"name": "TensorFlow", "description": "Production ML serving with TF Serving, TFLite for mobile deployment, and TFX pipelines."},
            {"name": "NLP", "description": "Transformer architectures, tokenization, fine-tuning LLMs, and prompt engineering."},
            {"name": "Computer Vision", "description": "Object detection, image segmentation, and medical imaging analysis with CNNs and Vision Transformers."},
            {"name": "Docker", "description": "ML model containerization and reproducible research environments."},
            {"name": "SQL", "description": "Complex analytical queries, data warehousing, and feature engineering for ML pipelines."},
        ],
        "projects": [
            {
                "title": "MedVision",
                "description": "An open-source computer vision library for medical image analysis. Includes pre-trained models for X-ray classification, tumor segmentation, and anomaly detection. Used by 3 university research labs.",
                "tags": ["docker"],
                "vote_total": 203,
                "vote_ratio": 98,
                "source_link": "https://github.com/priyasharma-ml/medvision",
                "demo_link": "https://medvision.readthedocs.io",
            },
            {
                "title": "PromptLab",
                "description": "A prompt engineering toolkit for evaluating and optimizing LLM prompts. Features A/B testing, automatic prompt variation generation, and cost tracking across OpenAI, Anthropic, and local models.",
                "tags": ["react", "django"],
                "vote_total": 156,
                "vote_ratio": 95,
                "source_link": "https://github.com/priyasharma-ml/promptlab",
            },
        ],
    },
    {
        "username": "jakethompson",
        "first_name": "Jake",
        "last_name": "Thompson",
        "email": "jake.thompson@outlook.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Jake Thompson",
            "location": "Toronto, Canada",
            "short_intro": "Frontend Architect @ Shopify | Design Systems & Accessibility",
            "bio": (
                "Frontend architect obsessed with pixel-perfect interfaces and inclusive design. "
                "At Shopify, I lead the design systems team responsible for Polaris — our component "
                "library used across 30+ internal apps. I've been building for the web since IE6 "
                "days and have seen every CSS hack in the book. These days I'm focused on building "
                "accessible, performant component libraries with React and Web Components. I believe "
                "accessibility isn't a feature — it's a requirement. Active W3C community contributor "
                "and WCAG advocate."
            ),
            "social_github": "https://github.com/jakethompsonui",
            "social_twitter": "https://twitter.com/jakethompsondev",
            "social_linkedin": "https://linkedin.com/in/jake-thompson-fe",
            "social_website": "https://jakethompson.design",
        },
        "skills": [
            {"name": "React", "description": "Component architecture, custom hooks, performance optimization, and server components."},
            {"name": "TypeScript", "description": "Advanced type patterns, generics, and type-safe API integrations for large codebases."},
            {"name": "CSS", "description": "Expert in modern CSS — Grid, Flexbox, Container Queries, and CSS-in-JS solutions."},
            {"name": "Accessibility", "description": "WCAG 2.1 AA compliance, screen reader testing, keyboard navigation, and ARIA patterns."},
            {"name": "Next.js", "description": "App Router, Server Components, ISR, and middleware — built multiple production e-commerce sites."},
            {"name": "Figma", "description": "Design-to-code workflow, component libraries, and design token management."},
            {"name": "Web Components", "description": "Custom elements, Shadow DOM, and framework-agnostic component libraries."},
        ],
        "projects": [
            {
                "title": "A11y Audit",
                "description": "An automated accessibility auditing tool that integrates into CI/CD pipelines. Scans web pages for WCAG 2.1 violations, generates detailed reports, and suggests fixes with code examples.",
                "tags": ["react", "typescript", "nextJS"],
                "vote_total": 94,
                "vote_ratio": 92,
                "source_link": "https://github.com/jakethompsonui/a11y-audit",
                "demo_link": "https://a11y-audit.vercel.app",
            },
            {
                "title": "Mosaic UI",
                "description": "A themeable, accessible React component library with 40+ components. Features dark mode, RTL support, and comprehensive Storybook documentation. 2.3K GitHub stars.",
                "tags": ["react", "typescript"],
                "vote_total": 178,
                "vote_ratio": 97,
                "source_link": "https://github.com/jakethompsonui/mosaic-ui",
                "demo_link": "https://mosaic-ui.dev",
            },
        ],
    },
    {
        "username": "aisakobayashi",
        "first_name": "Aisa",
        "last_name": "Kobayashi",
        "email": "aisa.kobayashi@gmail.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Aisa Kobayashi",
            "location": "Tokyo, Japan",
            "short_intro": "Mobile Engineer @ LINE | Flutter & Swift | Building for 200M+ users",
            "bio": (
                "Mobile engineer crafting experiences for one of Asia's largest messaging platforms. "
                "I specialize in cross-platform development with Flutter and native iOS with Swift. "
                "At LINE, I work on the core messaging features used by over 200 million people daily. "
                "Previously interned at Apple on the UIKit team. I'm a firm believer in offline-first "
                "architectures and smooth 60fps animations. Outside of work, I run a Japanese tech blog "
                "about mobile development with 15K subscribers and organize the Flutter Tokyo meetup."
            ),
            "social_github": "https://github.com/aisakobayashi",
            "social_twitter": "https://twitter.com/aisa_mobile",
            "social_linkedin": "https://linkedin.com/in/aisa-kobayashi",
            "social_youtube": "https://youtube.com/@aisamobile",
        },
        "skills": [
            {"name": "Flutter", "description": "Cross-platform mobile development with custom widgets, state management (Riverpod, Bloc), and platform channels."},
            {"name": "Swift", "description": "Native iOS development with SwiftUI, UIKit, Combine, and Core Data."},
            {"name": "Kotlin", "description": "Android development with Jetpack Compose, Coroutines, and Kotlin Multiplatform."},
            {"name": "Firebase", "description": "Authentication, Firestore, Cloud Functions, and analytics for mobile backends."},
            {"name": "GraphQL", "description": "Mobile-optimized GraphQL queries, caching with Apollo, and offline sync."},
            {"name": "CI/CD", "description": "Fastlane, GitHub Actions, and Bitrise for automated mobile builds and deployments."},
        ],
        "projects": [
            {
                "title": "FlutterVault",
                "description": "A production-ready Flutter starter template with authentication, state management, theming, localization, and CI/CD pre-configured. Includes 20+ reusable widgets and clean architecture patterns.",
                "tags": ["docker"],
                "vote_total": 134,
                "vote_ratio": 93,
                "source_link": "https://github.com/aisakobayashi/fluttervault",
                "demo_link": "https://fluttervault.dev",
            },
        ],
    },
    {
        "username": "davidokonkwo",
        "first_name": "David",
        "last_name": "Okonkwo",
        "email": "david.okonkwo@fastmail.com",
        "password": "devpass2026!",
        "profile": {
            "name": "David Okonkwo",
            "location": "Lagos, Nigeria",
            "short_intro": "DevOps Lead @ Paystack | Cloud Architecture | Terraform & K8s",
            "bio": (
                "DevOps engineer and cloud architect helping Africa's fastest-growing fintech "
                "scale reliably. At Paystack, I built the infrastructure that processes millions "
                "of transactions across 10 African markets. I specialize in infrastructure-as-code, "
                "observability, and building developer platforms that reduce deployment friction. "
                "Previously at Andela, where I helped establish SRE practices for distributed teams. "
                "I'm passionate about building Africa's tech ecosystem — I regularly mentor at "
                "DevCareer and speak at tech events across West Africa."
            ),
            "social_github": "https://github.com/davidokonkwo",
            "social_twitter": "https://twitter.com/david_devops",
            "social_linkedin": "https://linkedin.com/in/david-okonkwo",
            "social_website": "https://davidokonkwo.com",
        },
        "skills": [
            {"name": "Terraform", "description": "Infrastructure-as-code for AWS, GCP, and Azure. Managing 200+ resources across multiple environments."},
            {"name": "Kubernetes", "description": "Production cluster management, custom operators, and service mesh configuration with Istio."},
            {"name": "Docker", "description": "Container strategy, security scanning, and optimized image builds for microservice architectures."},
            {"name": "AWS", "description": "Solutions Architect certified. EKS, Lambda, DynamoDB, and multi-region architecture design."},
            {"name": "Python", "description": "Automation scripts, Lambda functions, and internal CLI tools for developer experience."},
            {"name": "Prometheus", "description": "Full observability stack — Prometheus, Grafana, Alertmanager, and custom metric exporters."},
            {"name": "Linux", "description": "System administration, kernel tuning, and performance profiling for production servers."},
        ],
        "projects": [
            {
                "title": "InfraBlueprint",
                "description": "A collection of production-ready Terraform modules for common cloud patterns — VPCs, EKS clusters, RDS setups, and CI/CD pipelines. Each module includes cost estimation and security best practices.",
                "tags": ["docker"],
                "vote_total": 89,
                "vote_ratio": 90,
                "source_link": "https://github.com/davidokonkwo/infrablueprint",
            },
            {
                "title": "ObserveStack",
                "description": "A one-command observability stack setup using Docker Compose. Deploys Prometheus, Grafana, Loki, and Tempo with pre-configured dashboards for common application metrics.",
                "tags": ["docker"],
                "vote_total": 67,
                "vote_ratio": 87,
                "source_link": "https://github.com/davidokonkwo/observestack",
                "demo_link": "https://observestack.dev",
            },
        ],
    },
    {
        "username": "sarahchen",
        "first_name": "Sarah",
        "last_name": "Chen",
        "email": "sarah.chen@pm.me",
        "password": "devpass2026!",
        "profile": {
            "name": "Sarah Chen",
            "location": "Seattle, WA",
            "short_intro": "Staff Engineer @ Figma | WebGL & Creative Coding | Ex-Google",
            "bio": (
                "Staff engineer working at the intersection of design tools and high-performance "
                "graphics. At Figma, I optimize the WebGL rendering engine that powers real-time "
                "collaborative design for millions of users. Before Figma, I spent 4 years at Google "
                "Chrome working on the rendering pipeline. I'm fascinated by creative coding, "
                "generative art, and pushing the boundaries of what's possible in a browser. My "
                'side projects have been featured in "Made with WebGL" and Codrops. I also teach a '
                'popular course on creative coding with Three.js.'
            ),
            "social_github": "https://github.com/sarahchen-gl",
            "social_twitter": "https://twitter.com/sarahchengl",
            "social_linkedin": "https://linkedin.com/in/sarah-chen-webgl",
            "social_youtube": "https://youtube.com/@sarahcreativecoding",
            "social_website": "https://sarahchen.art",
        },
        "skills": [
            {"name": "JavaScript", "description": "Deep expertise in vanilla JS, V8 internals, and browser APIs for high-performance applications."},
            {"name": "WebGL", "description": "Custom shaders, GPU-accelerated rendering, and real-time graphics programming."},
            {"name": "Three.js", "description": "3D web experiences, custom materials, post-processing effects, and VR/AR integrations."},
            {"name": "TypeScript", "description": "Large-scale TypeScript applications with strict type checking and generics."},
            {"name": "React", "description": "Performance-critical React applications with custom renderers and canvas integrations."},
            {"name": "C++", "description": "WASM compilation targets, performance-critical modules, and native browser engine work."},
            {"name": "GLSL", "description": "Custom vertex and fragment shaders for real-time visual effects and generative art."},
        ],
        "projects": [
            {
                "title": "ShaderPlayground",
                "description": "An interactive web-based GLSL shader editor with real-time preview, built-in tutorials, and a community gallery. Features hot-reloading, uniform controls, and export to image/video.",
                "tags": ["react", "typescript"],
                "vote_total": 245,
                "vote_ratio": 99,
                "source_link": "https://github.com/sarahchen-gl/shaderplayground",
                "demo_link": "https://shaderplayground.io",
            },
            {
                "title": "Particle Orchestra",
                "description": "A generative art piece that creates music-reactive particle systems using the Web Audio API and WebGL. 50K+ particles rendered at 60fps with custom physics simulation.",
                "tags": ["react"],
                "vote_total": 189,
                "vote_ratio": 97,
                "source_link": "https://github.com/sarahchen-gl/particle-orchestra",
                "demo_link": "https://particleorchestra.art",
            },
        ],
    },
    {
        "username": "lucasbergmann",
        "first_name": "Lucas",
        "last_name": "Bergmann",
        "email": "lucas.bergmann@posteo.de",
        "password": "devpass2026!",
        "profile": {
            "name": "Lucas Bergmann",
            "location": "Berlin, Germany",
            "short_intro": "Security Engineer @ Wire | Cryptography | Open Source Privacy Tools",
            "bio": (
                "Security engineer and privacy advocate building end-to-end encrypted communication "
                "platforms. At Wire, I work on the Proteus cryptographic protocol implementation and "
                "security audit infrastructure. My background is in applied cryptography — I completed "
                "my MSc at ETH Zurich focusing on post-quantum key exchange protocols. I contribute to "
                "several security-focused open-source projects and have discovered and responsibly "
                "disclosed vulnerabilities in popular libraries. I believe privacy is a fundamental "
                "right and build tools to protect it."
            ),
            "social_github": "https://github.com/lucasberg",
            "social_linkedin": "https://linkedin.com/in/lucas-bergmann-sec",
            "social_website": "https://lucasbergmann.dev",
        },
        "skills": [
            {"name": "Python", "description": "Security tooling, penetration testing frameworks, and cryptographic library implementations."},
            {"name": "Rust", "description": "Memory-safe systems programming for cryptographic libraries and security-critical applications."},
            {"name": "Cryptography", "description": "E2E encryption protocols, key management, TLS, and post-quantum algorithm research."},
            {"name": "Linux", "description": "Kernel hardening, SELinux policies, and secure server configuration."},
            {"name": "Go", "description": "Network security tools, reverse proxies, and high-performance scanning utilities."},
            {"name": "Docker", "description": "Secure container configurations, image scanning, and supply chain security."},
            {"name": "Penetration Testing", "description": "Web application security auditing, API fuzzing, and vulnerability assessment."},
        ],
        "projects": [
            {
                "title": "VaultGuard",
                "description": "A zero-knowledge password manager CLI built in Rust. Uses Argon2id for key derivation, XChaCha20-Poly1305 for encryption, and supports hardware key (YubiKey) authentication.",
                "tags": ["docker"],
                "vote_total": 156,
                "vote_ratio": 95,
                "source_link": "https://github.com/lucasberg/vaultguard",
            },
            {
                "title": "NetSentinel",
                "description": "A real-time network traffic analyzer and intrusion detection system written in Go. Features ML-based anomaly detection, customizable alert rules, and a web dashboard.",
                "tags": ["docker", "react"],
                "vote_total": 98,
                "vote_ratio": 91,
                "source_link": "https://github.com/lucasberg/netsentinel",
                "demo_link": "https://netsentinel.dev/demo",
            },
        ],
    },
    {
        "username": "oliviamartinez",
        "first_name": "Olivia",
        "last_name": "Martinez",
        "email": "olivia.martinez@tutanota.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Olivia Martinez",
            "location": "Barcelona, Spain",
            "short_intro": "Data Engineer @ Spotify | Apache Spark & dbt | Analytics at Scale",
            "bio": (
                "Data engineer building the pipelines that power Spotify's recommendation engine "
                "and creator analytics. I work with petabyte-scale datasets and real-time streaming "
                "systems that process billions of events daily. My expertise spans the modern data "
                "stack — from ingestion with Kafka to transformation with dbt to orchestration with "
                "Airflow. Previously at Datadog, where I built the metrics aggregation pipeline. I'm "
                "an active contributor to the dbt community and write about data engineering best "
                "practices on my blog. When offline, I'm likely hiking the Pyrenees or practicing "
                "flamenco guitar."
            ),
            "social_github": "https://github.com/oliviamartinez-data",
            "social_twitter": "https://twitter.com/olivia_data",
            "social_linkedin": "https://linkedin.com/in/olivia-martinez-data",
            "social_website": "https://oliviamartinez.dev",
        },
        "skills": [
            {"name": "Python", "description": "PySpark, Pandas, data pipeline development, and ETL automation."},
            {"name": "SQL", "description": "Advanced window functions, CTEs, query optimization, and data modeling."},
            {"name": "Apache Spark", "description": "Distributed data processing, Spark SQL, streaming, and performance tuning."},
            {"name": "dbt", "description": "Data transformation, testing, documentation, and analytics engineering best practices."},
            {"name": "Kafka", "description": "Real-time event streaming, consumer group management, and exactly-once processing."},
            {"name": "Airflow", "description": "Complex DAG design, custom operators, and production workflow orchestration."},
            {"name": "Docker", "description": "Data pipeline containerization and reproducible development environments."},
        ],
        "projects": [
            {
                "title": "DataForge",
                "description": "A modern data pipeline framework that simplifies building, testing, and deploying ETL workflows. Includes built-in data quality checks, lineage tracking, and Slack alerting.",
                "tags": ["docker", "django"],
                "vote_total": 118,
                "vote_ratio": 93,
                "source_link": "https://github.com/oliviamartinez-data/dataforge",
                "demo_link": "https://dataforge.dev",
            },
            {
                "title": "StreamLens",
                "description": "A real-time Kafka topic monitoring dashboard built with React and WebSockets. Features message inspection, consumer lag tracking, and partition distribution visualization.",
                "tags": ["react", "docker"],
                "vote_total": 82,
                "vote_ratio": 89,
                "source_link": "https://github.com/oliviamartinez-data/streamlens",
            },
        ],
    },
    {
        "username": "kwameansah",
        "first_name": "Kwame",
        "last_name": "Ansah",
        "email": "kwame.ansah@gmail.com",
        "password": "devpass2026!",
        "profile": {
            "name": "Kwame Ansah",
            "location": "Accra, Ghana",
            "short_intro": "Indie Hacker & Founder | Django & HTMX | Building SaaS in Africa",
            "bio": (
                "Full-stack developer and indie hacker building profitable SaaS products for the "
                "African market. I'm the founder of InvoiceGhana, a billing platform used by 2,000+ "
                "small businesses across West Africa. My tech stack is deliberately simple — Django, "
                "HTMX, and PostgreSQL — because shipping fast matters more than chasing trends. "
                "Previously a senior developer at Hubtel, where I worked on mobile money integration "
                "APIs. I'm a huge advocate for the HTMX/hypermedia approach and regularly write about "
                "building modern apps without heavy JavaScript frameworks. I also organize the "
                "Django Accra meetup."
            ),
            "social_github": "https://github.com/kwameansah",
            "social_twitter": "https://twitter.com/kwame_builds",
            "social_linkedin": "https://linkedin.com/in/kwame-ansah",
            "social_youtube": "https://youtube.com/@kwamebuilds",
            "social_website": "https://kwameansah.com",
        },
        "skills": [
            {"name": "Django", "description": "Full-stack Django development — from MVT to DRF. Built and shipped 5 production SaaS applications."},
            {"name": "Python", "description": "Backend development, API design, scripting, and payment integration libraries."},
            {"name": "HTMX", "description": "Modern interactive UIs without JavaScript frameworks. Converted SPAs to HTMX with 60% less code."},
            {"name": "PostgreSQL", "description": "Database architecture, partitioning strategies, and full-text search implementations."},
            {"name": "JavaScript", "description": "Progressive enhancement, Alpine.js, and vanilla JS for interactive components."},
            {"name": "Tailwind CSS", "description": "Rapid UI prototyping and production styling. Built custom design systems with Tailwind."},
            {"name": "Stripe API", "description": "Payment processing, subscription management, and webhook handling for SaaS billing."},
        ],
        "projects": [
            {
                "title": "InvoiceGhana",
                "description": "A billing and invoicing platform designed for West African SMEs. Features mobile money integration (MTN, Vodafone), multi-currency support, tax compliance, and PDF generation.",
                "tags": ["django", "htmx", "docker"],
                "vote_total": 143,
                "vote_ratio": 94,
                "source_link": "https://github.com/kwameansah/invoiceghana",
                "demo_link": "https://invoiceghana.com",
            },
            {
                "title": "DjangoShipFast",
                "description": "A Django SaaS boilerplate with authentication, billing, teams, admin dashboard, and email templates pre-configured. Go from idea to production in hours, not weeks.",
                "tags": ["django", "htmx"],
                "vote_total": 201,
                "vote_ratio": 96,
                "source_link": "https://github.com/kwameansah/djangoshipfast",
                "demo_link": "https://djangoshipfast.com",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with 10 realistic developer profiles, skills, and projects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all seeded users before creating new ones.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Disconnect the post_save signal to avoid sending emails
        # and the broken user.name attribute access
        post_save.disconnect(create_profile, sender=User)

        try:
            self._seed(options)
        finally:
            # Reconnect the signal
            post_save.connect(create_profile, sender=User)

    def _seed(self, options):
        usernames = [dev["username"] for dev in DEVELOPERS]

        if options["clear"]:
            deleted_count = User.objects.filter(username__in=usernames).delete()[0]
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing seeded objects."))

        created_count = 0
        skipped_count = 0

        for dev_data in DEVELOPERS:
            if User.objects.filter(username=dev_data["username"]).exists():
                self.stdout.write(self.style.WARNING(f"  Skipping {dev_data['username']} (already exists)"))
                skipped_count += 1
                continue

            # Create User
            user = User(
                username=dev_data["username"],
                first_name=dev_data["first_name"],
                last_name=dev_data["last_name"],
                email=dev_data["email"],
            )
            user.set_password(dev_data["password"])
            user.save()

            # Create Profile
            profile_data = dev_data["profile"]
            profile = Profile.objects.create(
                user=user,
                name=profile_data["name"],
                email=dev_data["email"],
                username=dev_data["username"],
                location=profile_data.get("location", ""),
                short_intro=profile_data.get("short_intro", ""),
                bio=profile_data.get("bio", ""),
                social_github=profile_data.get("social_github", ""),
                social_twitter=profile_data.get("social_twitter", ""),
                social_linkedin=profile_data.get("social_linkedin", ""),
                social_youtube=profile_data.get("social_youtube", ""),
                social_website=profile_data.get("social_website", ""),
            )

            # Create Skills
            for skill_data in dev_data.get("skills", []):
                Skill.objects.create(
                    owner=profile,
                    name=skill_data["name"],
                    description=skill_data["description"],
                )

            # Create Projects
            for proj_data in dev_data.get("projects", []):
                project = Project.objects.create(
                    owner=profile,
                    title=proj_data["title"],
                    description=proj_data.get("description", ""),
                    demo_link=proj_data.get("demo_link", ""),
                    source_link=proj_data.get("source_link", ""),
                    vote_total=proj_data.get("vote_total", 0),
                    vote_ratio=proj_data.get("vote_ratio", 0),
                )
                # Add tags
                for tag_name in proj_data.get("tags", []):
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"  ✓ Created {dev_data['profile']['name']} "
                f"(@{dev_data['username']}) — "
                f"{len(dev_data.get('skills', []))} skills, "
                f"{len(dev_data.get('projects', []))} projects"
            ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Done! Created {created_count} developers, skipped {skipped_count}."))
