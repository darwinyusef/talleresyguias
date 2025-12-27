# ADR + TOGAF + Scrum: Parte 2 - Automatización e Implementación

## Índice
6. [Herramientas de Automatización](#6-automation)
7. [Casos de Uso Reales](#7-casos-uso)
8. [Implementación Paso a Paso](#8-implementation)
9. [Métricas y KPIs](#9-metrics)
10. [Anti-patterns y Soluciones](#10-antipatterns)

---

## 6. Herramientas de Automatización

### CLI Tool Completo para ADR + TOGAF + Scrum

```python
import click
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import yaml

# ==========================================
# ADR + TOGAF + SCRUM CLI
# ==========================================

class ADRTOGAFScrum CLI:
    """
    CLI tool para gestionar ADRs integrados con TOGAF y Scrum

    Comandos:
    - adr init: Initialize ADR repository
    - adr new: Create new ADR
    - adr list: List all ADRs
    - adr review: Prepare Architecture Board review
    - adr metrics: Show metrics and compliance
    - sprint plan: Create sprint planning template with ADRs
    - sprint review: Generate sprint review report
    - togaf vision: Create architecture vision
    - governance check: Check compliance with policies
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.adr_dir = self.repo_path / "docs" / "architecture" / "decisions"
        self.togaf_dir = self.repo_path / "docs" / "architecture" / "togaf"
        self.sprint_dir = self.repo_path / "docs" / "sprints"
        self.config_file = self.repo_path / ".adr-config.yaml"

    # ========================================
    # INITIALIZATION
    # ========================================

    def init(self):
        """Initialize ADR + TOGAF repository structure"""
        print("🚀 Initializing ADR + TOGAF + Scrum repository...\n")

        # Create directory structure
        directories = [
            self.adr_dir,
            self.togaf_dir / "vision",
            self.togaf_dir / "principles",
            self.togaf_dir / "building-blocks",
            self.sprint_dir,
            self.repo_path / "docs" / "governance"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")

        # Create config file
        config = {
            "project_name": "My Project",
            "architecture_board": [
                "CTO",
                "Lead Architect"
            ],
            "governance_levels": {
                "team": {
                    "approvers": ["Tech Lead"],
                    "max_cost": 1000
                },
                "technical": {
                    "approvers": ["Lead Architect"],
                    "max_cost": 5000
                },
                "tactical": {
                    "approvers": ["Architecture Board"],
                    "max_cost": 10000
                },
                "strategic": {
                    "approvers": ["Architecture Board", "CTO"],
                    "max_cost": 50000
                }
            },
            "togaf_principles": [
                "Cloud-native first",
                "API-first design",
                "Security by default",
                "Cost-effective"
            ],
            "sprint_duration_weeks": 2,
            "current_sprint": 1
        }

        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        print(f"\n  ✅ Created config: {self.config_file}")

        # Create README
        readme_content = """# Architecture Documentation

This repository contains architecture documentation using:
- **ADRs (Architecture Decision Records)**: Lightweight decision documentation
- **TOGAF ADM**: Strategic architecture framework (adapted for Agile)
- **Scrum**: Agile development methodology

## Structure

- `docs/architecture/decisions/`: ADRs
- `docs/architecture/togaf/`: TOGAF artifacts (Vision, Principles, Building Blocks)
- `docs/sprints/`: Sprint planning and review documents
- `docs/governance/`: Governance policies and board reviews

## Quick Start

```bash
# Create new ADR
adr new "Database Selection for User Service"

# Create sprint planning
sprint plan --sprint 5 --goal "Implement user authentication"

# Check governance compliance
governance check --adr 15

# Generate Architecture Board review
adr review --month 12
```

## Documentation

- [ADR Template](docs/architecture/decisions/template.md)
- [TOGAF Principles](docs/architecture/togaf/principles/README.md)
- [Governance Model](docs/governance/README.md)
"""

        readme_file = self.repo_path / "docs" / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)

        print(f"  ✅ Created README: {readme_file}")

        print("\n✅ Initialization complete!\n")
        print("Next steps:")
        print("  1. Edit .adr-config.yaml with your project details")
        print("  2. Create your first ADR: adr new 'Your Decision'")
        print("  3. Create architecture vision: togaf vision")

    # ========================================
    # ADR MANAGEMENT
    # ========================================

    def create_adr(
        self,
        title: str,
        sprint: Optional[int] = None,
        user_story: Optional[str] = None,
        governance_level: str = "technical",
        template: str = "standard"
    ) -> int:
        """Create new ADR"""

        # Get next ADR number
        existing_adrs = list(self.adr_dir.glob("ADR-*.md"))
        adr_number = len(existing_adrs) + 1

        # Load config
        config = self._load_config()

        # Determine sprint
        if sprint is None:
            sprint = config.get("current_sprint", 1)

        # Generate filename
        filename = f"ADR-{adr_number:04d}-{self._slugify(title)}.md"
        filepath = self.adr_dir / filename

        # Select template
        content = self._get_adr_template(
            adr_number=adr_number,
            title=title,
            sprint=sprint,
            user_story=user_story,
            governance_level=governance_level,
            config=config,
            template_type=template
        )

        # Write file
        with open(filepath, 'w') as f:
            f.write(content)

        print(f"\n✅ Created ADR-{adr_number:04d}: {title}")
        print(f"   File: {filepath}")
        print(f"   Sprint: {sprint}")
        print(f"   Governance: {governance_level}")
        print(f"\nNext steps:")
        print(f"  1. Edit {filepath}")
        print(f"  2. Add options considered")
        print(f"  3. Document decision and rationale")
        print(f"  4. Get approval: adr approve {adr_number}")

        return adr_number

    def _get_adr_template(
        self,
        adr_number: int,
        title: str,
        sprint: int,
        user_story: Optional[str],
        governance_level: str,
        config: Dict,
        template_type: str
    ) -> str:
        """Generate ADR content from template"""

        approvers = config['governance_levels'][governance_level]['approvers']
        principles = config['togaf_principles']

        template = f"""# ADR-{adr_number:04d}: {title}

**Fecha:** {datetime.now().strftime('%Y-%m-%d')}
**Sprint:** Sprint {sprint}
**Estado:** Draft
**Nivel de Governance:** {governance_level}

## Contexto y Problema

**User Story:** {user_story or 'TBD'}

**Problema arquitectónico:**
[Describe el problema o decisión que necesita ser tomada]

**Ejemplo:**
Para implementar [feature], necesitamos decidir [what needs to be decided].

## Factores de Decisión

Prioridad:
1. ⭐⭐⭐ [Factor crítico 1]
2. ⭐⭐ [Factor importante 2]
3. ⭐ [Factor nice-to-have 3]

## Opciones Consideradas

### Opción 1: [Nombre]

**Descripción:** [Breve descripción]

**Pros:**
- ✅ [Pro 1]
- ✅ [Pro 2]

**Cons:**
- ❌ [Con 1]
- ❌ [Con 2]

**Costo:** $[X]/month or $[Y] one-time
**Complejidad:** Low | Medium | High
**Riesgo:** Low | Medium | High

### Opción 2: [Nombre]

[Similar structure...]

### Opción 3: [Nombre]

[Similar structure...]

## Decisión

**Elegimos:** [Opción seleccionada]

**Rationale:**
[¿Por qué esta opción es la mejor para nuestro contexto?]

**Implementación:**
[Cómo la vamos a implementar en este sprint]

## Consecuencias

### Positivas ✅
- [Consecuencia positiva 1]
- [Consecuencia positiva 2]

### Negativas ⚠️
- [Consecuencia negativa 1] → Mitigación: [cómo la mitigamos]
- [Consecuencia negativa 2] → Mitigación: [cómo la mitigamos]

### Riesgos 🔥
- [Riesgo 1] → Plan: [contingencia]
- [Riesgo 2] → Plan: [contingencia]

## Compliance con TOGAF Principles

"""

        # Add TOGAF principles checkboxes
        for principle in principles:
            template += f"- [ ] {principle}\n"

        template += """
**Notas:** [Explicar cualquier principio que no se cumpla y por qué]

## Stakeholders

**Deciders:** [Quienes toman la decisión]
**Consulted:** [Quienes deben ser consultados]
**Informed:** [Quienes deben ser informados]

## Aprobación

"""

        # Add approval checkboxes
        for approver in approvers:
            template += f"- [ ] {approver} approval\n"

        template += f"""
## Referencias

- Spike results: [link a documentación de spike]
- Related ADRs: [ADR-XXX, ADR-YYY]
- TOGAF phase: [Phase X]
- Epic: [EPIC-ID]
- User Story: {user_story or '[US-ID]'}

## Metadata

```yaml
adr_number: {adr_number}
title: "{title}"
status: "Draft"
sprint: {sprint}
governance_level: "{governance_level}"
created_date: "{datetime.now().isoformat()}"
```
"""

        return template

    def list_adrs(
        self,
        status: Optional[str] = None,
        sprint: Optional[int] = None,
        governance_level: Optional[str] = None
    ):
        """List all ADRs with filters"""

        adrs = self._load_all_adrs()

        # Apply filters
        if status:
            adrs = [adr for adr in adrs if adr.get('status') == status]
        if sprint:
            adrs = [adr for adr in adrs if adr.get('sprint') == sprint]
        if governance_level:
            adrs = [adr for adr in adrs if adr.get('governance_level') == governance_level]

        print(f"\n📄 ADRs Found: {len(adrs)}\n")

        # Group by status
        by_status = {}
        for adr in adrs:
            status_key = adr.get('status', 'Unknown')
            if status_key not in by_status:
                by_status[status_key] = []
            by_status[status_key].append(adr)

        # Display grouped
        for status_key, status_adrs in by_status.items():
            print(f"## {status_key} ({len(status_adrs)})\n")

            for adr in sorted(status_adrs, key=lambda x: x.get('adr_number', 0)):
                status_icon = {
                    'Draft': '📝',
                    'Proposed': '🤔',
                    'Accepted': '✅',
                    'Rejected': '❌',
                    'Superseded': '🔄'
                }.get(status_key, '❓')

                print(f"{status_icon} ADR-{adr['adr_number']:04d}: {adr['title']}")
                print(f"   Sprint: {adr.get('sprint', 'N/A')} | "
                      f"Governance: {adr.get('governance_level', 'N/A')} | "
                      f"Created: {adr.get('created_date', 'N/A')[:10]}")
                print()

    def _load_all_adrs(self) -> List[Dict]:
        """Load all ADRs and extract metadata"""
        adrs = []

        for adr_file in sorted(self.adr_dir.glob("ADR-*.md")):
            try:
                with open(adr_file, 'r') as f:
                    content = f.read()

                # Extract metadata from YAML block
                metadata = self._extract_metadata(content)

                if metadata:
                    metadata['filepath'] = str(adr_file)
                    adrs.append(metadata)
            except Exception as e:
                print(f"Warning: Could not load {adr_file}: {e}")

        return adrs

    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract metadata from ADR markdown file"""
        import re

        # Try to find YAML metadata block
        yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)

        if yaml_match:
            try:
                metadata = yaml.safe_load(yaml_match.group(1))
                return metadata
            except:
                pass

        # Fallback: extract from headers
        metadata = {}

        # Extract ADR number from title
        title_match = re.search(r'# ADR-(\d+): (.+)', content)
        if title_match:
            metadata['adr_number'] = int(title_match.group(1))
            metadata['title'] = title_match.group(2).strip()

        # Extract status
        status_match = re.search(r'\*\*Estado:\*\* (.+)', content)
        if status_match:
            metadata['status'] = status_match.group(1).strip()

        # Extract sprint
        sprint_match = re.search(r'\*\*Sprint:\*\* Sprint (\d+)', content)
        if sprint_match:
            metadata['sprint'] = int(sprint_match.group(1))

        # Extract governance level
        gov_match = re.search(r'\*\*Nivel de Governance:\*\* (\w+)', content)
        if gov_match:
            metadata['governance_level'] = gov_match.group(1).strip()

        return metadata if metadata else None

    # ========================================
    # ARCHITECTURE BOARD REVIEW
    # ========================================

    def generate_board_review(self, month: int, year: int):
        """Generate Architecture Board review document"""

        print(f"\n📋 Generating Architecture Board Review for {year}-{month:02d}...\n")

        # Load all ADRs from the month
        adrs = self._load_all_adrs()

        month_adrs = [
            adr for adr in adrs
            if adr.get('created_date', '').startswith(f"{year}-{month:02d}")
        ]

        if not month_adrs:
            print(f"❌ No ADRs found for {year}-{month:02d}")
            return

        config = self._load_config()

        # Generate review document
        review_content = f"""# Architecture Board Review - {year}-{month:02d}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Attendees:** {', '.join(config['architecture_board'])}
**Duration:** 2 hours

## Summary

Total ADRs for Review: {len(month_adrs)}

By Status:
"""

        # Count by status
        status_counts = {}
        for adr in month_adrs:
            status = adr.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        for status, count in status_counts.items():
            review_content += f"- {status}: {count}\n"

        review_content += "\nBy Governance Level:\n"

        # Count by governance level
        gov_counts = {}
        for adr in month_adrs:
            gov_level = adr.get('governance_level', 'Unknown')
            gov_counts[gov_level] = gov_counts.get(gov_level, 0) + 1

        for gov_level, count in gov_counts.items():
            review_content += f"- {gov_level}: {count}\n"

        review_content += "\n---\n\n## ADRs for Review\n\n"

        # Add each ADR
        for i, adr in enumerate(sorted(month_adrs, key=lambda x: x.get('adr_number', 0)), 1):
            review_content += f"""### {i}. ADR-{adr['adr_number']:04d}: {adr['title']}

**Sprint:** Sprint {adr.get('sprint', 'N/A')}
**Status:** {adr.get('status', 'Unknown')}
**Governance Level:** {adr.get('governance_level', 'Unknown')}
**Created:** {adr.get('created_date', 'N/A')[:10]}

**Decision Summary:**
[To be filled during review by reading the ADR]

**Compliance Check:**

| Principle | Compliant? | Notes |
|-----------|------------|-------|
"""

            for principle in config['togaf_principles']:
                review_content += f"| {principle} | [ ] Yes / [ ] No | |\n"

            review_content += """
**Board Decision:**

- [ ] ✅ Approved
- [ ] ⚠️ Approved with conditions: ________________________________
- [ ] ❌ Rejected: ________________________________
- [ ] 🔄 Request changes: ________________________________

**Action Items:**
- [ ] [Action] - Owner: _________ - Deadline: _________

---

"""

        # Add compliance report section
        review_content += """## Compliance Report

**Overall Compliance:** ___% of ADRs fully compliant

**Top Violations:**
1. [Violation type]: [N] occurrences
2. [Violation type]: [M] occurrences

**Analysis:**
[To be completed during review]

## Strategic Recommendations

1. [Recommendation based on patterns observed]
2. [Recommendation based on patterns observed]

## Action Items Summary

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Action 1] | [Owner] | [Date] | [ ] |
| [Action 2] | [Owner] | [Date] | [ ] |

## Next Month Focus

- [Focus area 1 based on roadmap]
- [Focus area 2 based on roadmap]

---

**Next Review:** [Date next month]
"""

        # Save review document
        review_filename = f"architecture-board-review-{year}-{month:02d}.md"
        review_filepath = self.repo_path / "docs" / "governance" / review_filename

        with open(review_filepath, 'w') as f:
            f.write(review_content)

        print(f"✅ Review document created: {review_filepath}")
        print(f"\n📊 Summary:")
        print(f"  Total ADRs: {len(month_adrs)}")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")

        print(f"\nNext steps:")
        print(f"  1. Distribute review document to Architecture Board")
        print(f"  2. Schedule review meeting")
        print(f"  3. Complete compliance checks during meeting")
        print(f"  4. Update ADR statuses based on board decisions")

    # ========================================
    # SPRINT PLANNING
    # ========================================

    def create_sprint_planning(
        self,
        sprint_number: int,
        sprint_goal: str,
        user_stories: List[str]
    ):
        """Create sprint planning document with ADR templates"""

        print(f"\n📅 Creating Sprint {sprint_number} Planning Document...\n")

        config = self._load_config()

        # Update current sprint in config
        config['current_sprint'] = sprint_number
        self._save_config(config)

        # Calculate sprint dates
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=config['sprint_duration_weeks'])

        planning_content = f"""# Sprint {sprint_number} Planning

**Date:** {start_date.strftime('%Y-%m-%d')}
**Duration:** {config['sprint_duration_weeks']} weeks ({start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')})
**Team:** [Team members]

## Sprint Goal

{sprint_goal}

## Capacity

- Team size: [N] people
- Capacity: [N * 10] story points
- Planned: [X] story points
- Buffer: [Y] story points for unknowns

## User Stories

### Committed

| ID | Title | Points | Architecture Decisions | ADR |
|----|-------|--------|------------------------|-----|
"""

        # Add user stories
        for story in user_stories:
            planning_content += f"| {story} | [Points] | [Decision if needed] | [ADR-XXX] |\n"

        planning_content += """
### Stretch Goals

[Stories we'll do if we have time]

## Architecture Decisions Needed

[To be identified during planning - use: adr new "Decision Title" --sprint {sprint_number}]

## Spikes

| Spike | ADR | Assignee | Timebox | Outcome |
|-------|-----|----------|---------|---------|
| [Spike title] | [ADR-XXX] | [Name] | [4h] | [Update ADR with findings] |

## Dependencies

- [Dependency 1]
- [External dependency]

## Definition of Done

- [ ] Code written & reviewed
- [ ] Tests passing (unit + integration)
- [ ] ADRs finalized and approved
- [ ] Documentation updated
- [ ] Deployed to staging

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [Mitigation strategy] |

---

## Planning Notes

[Notes from planning meeting]

## Action Items

- [ ] [Action 1] - Owner: [Name] - Deadline: [Date]
- [ ] [Action 2] - Owner: [Name] - Deadline: [Date]
"""

        # Save planning document
        planning_filename = f"sprint-{sprint_number:02d}-planning.md"
        planning_filepath = self.sprint_dir / planning_filename

        with open(planning_filepath, 'w') as f:
            f.write(planning_content)

        print(f"✅ Sprint planning document created: {planning_filepath}")
        print(f"\nSprint {sprint_number} Details:")
        print(f"  Goal: {sprint_goal}")
        print(f"  Duration: {config['sprint_duration_weeks']} weeks")
        print(f"  Start: {start_date.strftime('%Y-%m-%d')}")
        print(f"  End: {end_date.strftime('%Y-%m-%d')}")

        print(f"\nNext steps:")
        print(f"  1. Review and refine user stories")
        print(f"  2. Identify architecture decisions needed")
        print(f"  3. Create ADRs: adr new 'Decision Title' --sprint {sprint_number}")
        print(f"  4. Plan spikes for complex decisions")
        print(f"  5. Estimate and commit to stories")

    def create_sprint_review(self, sprint_number: int):
        """Create sprint review document"""

        print(f"\n📊 Creating Sprint {sprint_number} Review Document...\n")

        # Load ADRs from this sprint
        adrs = self._load_all_adrs()
        sprint_adrs = [adr for adr in adrs if adr.get('sprint') == sprint_number]

        review_content = f"""# Sprint {sprint_number} Review

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Stakeholders:** [Product Owner, CTO, etc.]

## Sprint Goal

[Sprint goal from planning]

**Status:** [ ] ✅ Achieved | [ ] ⚠️ Partially | [ ] ❌ Not achieved

## Demo

[Demo notes - what was demonstrated]

## Completed User Stories

| ID | Title | Points | Status |
|----|-------|--------|--------|
| [US-ID] | [Title] | [Points] | ✅ Done |

**Velocity:** [Points completed] / [Points committed] = [X]%

## Architecture Decisions Made

Total ADRs this sprint: {len(sprint_adrs)}

"""

        for adr in sorted(sprint_adrs, key=lambda x: x.get('adr_number', 0)):
            review_content += f"""### ADR-{adr['adr_number']:04d}: {adr['title']}

**Status:** {adr.get('status', 'Unknown')}
**Governance Level:** {adr.get('governance_level', 'Unknown')}

**Context:** [Brief context]

**Decision:** [What we decided]

**Impact:**
- Performance: [Impact]
- Cost: [$ impact]
- Complexity: [Low/Medium/High]
- Team velocity: [Impact on development speed]

**Demo:** [Link to working demo if applicable]

---

"""

        review_content += """## Escalations to Architecture Board

The following decisions require Board approval:

[List ADRs that need board approval]

## Stakeholder Feedback

**Feedback received:**
- [Feedback 1]
- [Feedback 2]

**Action items:**
- [ ] [Action based on feedback] - Owner: [Name]

## Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Velocity | [X] pts | [Y] pts | ✅/⚠️/❌ |
| ADRs completed | [N] | [M] | ✅/⚠️/❌ |
| Test coverage | 80% | [X]% | ✅/⚠️/❌ |
| Deploy frequency | [N]/week | [M]/week | ✅/⚠️/❌ |

## Lessons Learned

**What went well:**
- [Success 1]
- [Success 2]

**What to improve:**
- [Improvement 1]
- [Improvement 2]

## Next Sprint Preview

**Sprint Goal:** [Next sprint goal]

**Planned Work:**
- [Epic/story 1]
- [Epic/story 2]

**Architecture Decisions Needed:**
- [Expected decision 1]
- [Expected decision 2]

---

**Next Review:** [Date + 2 weeks]
"""

        # Save review document
        review_filename = f"sprint-{sprint_number:02d}-review.md"
        review_filepath = self.sprint_dir / review_filename

        with open(review_filepath, 'w') as f:
            f.write(review_content)

        print(f"✅ Sprint review document created: {review_filepath}")
        print(f"\n📊 Sprint {sprint_number} Summary:")
        print(f"  ADRs created: {len(sprint_adrs)}")

        if sprint_adrs:
            status_counts = {}
            for adr in sprint_adrs:
                status = adr.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1

            for status, count in status_counts.items():
                print(f"  {status}: {count}")

    # ========================================
    # TOGAF MANAGEMENT
    # ========================================

    def create_architecture_vision(self):
        """Create TOGAF Architecture Vision document"""

        print("\n🎯 Creating Architecture Vision Document...\n")

        config = self._load_config()

        vision_content = f"""# Architecture Vision - {config['project_name']}

**Version:** 1.0
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Authors:** [Architecture Team]
**Stakeholders:** {', '.join(config['architecture_board'])}

## Executive Summary

[1 paragraph vision statement - what are we building and why]

## Business Drivers

1. **[Driver 1]:** [Description]
   - Metric: [How we measure success]
   - Timeline: [When we need to achieve this]

2. **[Driver 2]:** [Description]
   - Metric: [How we measure success]
   - Timeline: [When we need to achieve this]

## Architecture Vision Statement

[2-3 paragraph description of target architecture]

**Example:**
Cloud-native microservices platform on AWS enabling rapid feature delivery
through autonomous teams. Event-driven architecture with Kafka for async
communication. Database per service for independence. Kubernetes for
orchestration and scaling.

## Architecture Principles

"""

        for i, principle in enumerate(config['togaf_principles'], 1):
            vision_content += f"""{i}. **{principle}**
   - Rationale: [Why this matters]
   - Implications: [What this means for implementation]

"""

        vision_content += """## Target Architecture (High-Level)

### Application Architecture
- **Style:** [Microservices | Modular Monolith | etc.]
- **Key Services:** [List of core services]
- **Integration:** [REST APIs | Events | GraphQL]

### Data Architecture
- **Strategy:** [Database per service | Shared database | etc.]
- **Databases:** [PostgreSQL, Redis, etc.]
- **Events:** [Kafka for async communication]

### Technology Architecture
- **Cloud:** [AWS | GCP | Azure]
- **Compute:** [EKS | ECS | Lambda]
- **Observability:** [Prometheus, Grafana, Jaeger]

## Roadmap (Quarterly)

| Quarter | Focus | Key Deliverables | Success Metrics |
|---------|-------|------------------|-----------------|
| Q1 | Foundation | Infrastructure, CI/CD | [Metrics] |
| Q2 | Features | Business logic | [Metrics] |
| Q3 | Scale | Performance, Reliability | [Metrics] |
| Q4 | Launch | Production release | [Metrics] |

## Success Metrics

- [ ] Time to market: < [X] months
- [ ] System availability: > 99.9%
- [ ] Deploy frequency: > [N]/day
- [ ] Lead time for changes: < [X] days
- [ ] MTTR: < [X] minutes

## Constraints

- **Budget:** $[X]
- **Team Size:** [N] engineers
- **Timeline:** [X] months
- **Compliance:** [PCI-DSS, HIPAA, GDPR, etc.]
- **Technical:** [Technology constraints]

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

## Stakeholder Analysis

| Stakeholder | Interest | Influence | Engagement Strategy |
|-------------|----------|-----------|---------------------|
| [Stakeholder 1] | [High/Med/Low] | [High/Med/Low] | [Strategy] |

## Next Steps

1. [ ] Review and approve vision (Architecture Board)
2. [ ] Create target architecture (Phases B-D)
3. [ ] Convert to product backlog
4. [ ] Begin Sprint 0 (infrastructure foundation)

---

**Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {datetime.now().strftime('%Y-%m-%d')} | [Author] | Initial version |
"""

        # Save vision document
        vision_filepath = self.togaf_dir / "vision" / "architecture-vision.md"

        with open(vision_filepath, 'w') as f:
            f.write(vision_content)

        print(f"✅ Architecture vision created: {vision_filepath}")
        print(f"\nNext steps:")
        print(f"  1. Edit and complete the vision document")
        print(f"  2. Review with Architecture Board")
        print(f"  3. Create target architecture")
        print(f"  4. Convert vision to product backlog epics")

    # ========================================
    # GOVERNANCE & METRICS
    # ========================================

    def check_governance(self, adr_number: Optional[int] = None):
        """Check governance compliance"""

        print("\n⚖️  Checking Governance Compliance...\n")

        config = self._load_config()
        adrs = self._load_all_adrs()

        if adr_number:
            adrs = [adr for adr in adrs if adr.get('adr_number') == adr_number]

        if not adrs:
            print("❌ No ADRs found")
            return

        violations = []

        for adr in adrs:
            adr_violations = []

            # Check 1: Governance level vs approvers
            gov_level = adr.get('governance_level', 'technical')
            required_approvers = config['governance_levels'].get(gov_level, {}).get('approvers', [])

            # Would need to parse ADR content to check if approvals are marked
            # Simplified for this example

            # Check 2: TOGAF principles compliance
            # Would need to parse ADR content to check principle checkboxes
            # Simplified for this example

            # Check 3: Required fields
            required_fields = ['title', 'status', 'sprint', 'governance_level']
            for field in required_fields:
                if not adr.get(field):
                    adr_violations.append(f"Missing required field: {field}")

            if adr_violations:
                violations.append({
                    'adr': f"ADR-{adr['adr_number']:04d}",
                    'title': adr.get('title', 'Unknown'),
                    'violations': adr_violations
                })

        # Report
        if not violations:
            print("✅ All ADRs are compliant!\n")
        else:
            print(f"⚠️  Found {len(violations)} ADRs with violations:\n")

            for v in violations:
                print(f"❌ {v['adr']}: {v['title']}")
                for violation in v['violations']:
                    print(f"   - {violation}")
                print()

    def show_metrics(self):
        """Show architecture metrics and KPIs"""

        print("\n📊 Architecture Metrics Dashboard\n")
        print("="*60)

        adrs = self._load_all_adrs()

        # Metric 1: Total ADRs
        print(f"\n📄 Total ADRs: {len(adrs)}\n")

        # Metric 2: By Status
        print("By Status:")
        status_counts = {}
        for adr in adrs:
            status = adr.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        for status, count in sorted(status_counts.items()):
            percentage = (count / len(adrs) * 100) if adrs else 0
            print(f"  {status:15s}: {count:3d} ({percentage:5.1f}%)")

        # Metric 3: By Governance Level
        print("\nBy Governance Level:")
        gov_counts = {}
        for adr in adrs:
            gov_level = adr.get('governance_level', 'Unknown')
            gov_counts[gov_level] = gov_counts.get(gov_level, 0) + 1

        for gov_level, count in sorted(gov_counts.items()):
            percentage = (count / len(adrs) * 100) if adrs else 0
            print(f"  {gov_level:15s}: {count:3d} ({percentage:5.1f}%)")

        # Metric 4: By Sprint
        print("\nBy Sprint (last 5 sprints):")
        sprint_counts = {}
        for adr in adrs:
            sprint = adr.get('sprint', 0)
            if sprint:
                sprint_counts[sprint] = sprint_counts.get(sprint, 0) + 1

        for sprint in sorted(sprint_counts.keys(), reverse=True)[:5]:
            count = sprint_counts[sprint]
            print(f"  Sprint {sprint:2d}: {count:3d} ADRs")

        # Metric 5: Decision velocity
        print("\n⚡ Decision Velocity:")
        accepted_adrs = [adr for adr in adrs if adr.get('status') == 'Accepted']
        print(f"  Accepted ADRs: {len(accepted_adrs)} / {len(adrs)} ({len(accepted_adrs)/len(adrs)*100:.1f}%)")

        # Metric 6: Compliance rate
        print("\n✅ Compliance:")
        compliant_count = len([adr for adr in adrs if self._is_compliant(adr)])
        compliance_rate = (compliant_count / len(adrs) * 100) if adrs else 0
        print(f"  Compliant ADRs: {compliant_count} / {len(adrs)} ({compliance_rate:.1f}%)")

        print("\n" + "="*60)

    def _is_compliant(self, adr: Dict) -> bool:
        """Check if ADR is compliant (simplified)"""
        required_fields = ['title', 'status', 'sprint', 'governance_level']
        return all(adr.get(field) for field in required_fields)

    # ========================================
    # HELPER METHODS
    # ========================================

    def _load_config(self) -> Dict:
        """Load configuration"""
        if not self.config_file.exists():
            return {}

        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def _save_config(self, config: Dict):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def _slugify(self, text: str) -> str:
        """Convert text to slug"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text[:50]  # Limit length

# ==========================================
# CLI INTERFACE
# ==========================================

@click.group()
def cli():
    """ADR + TOGAF + Scrum CLI Tool"""
    pass

@cli.command()
def init():
    """Initialize ADR + TOGAF repository"""
    tool = ADRTOGAFScrumCLI()
    tool.init()

@cli.command()
@click.argument('title')
@click.option('--sprint', type=int, help='Sprint number')
@click.option('--story', help='User story ID')
@click.option('--governance', default='technical',
              type=click.Choice(['team', 'technical', 'tactical', 'strategic']))
@click.option('--template', default='standard', help='Template to use')
def new(title, sprint, story, governance, template):
    """Create new ADR"""
    tool = ADRTOGAFScrumCLI()
    tool.create_adr(
        title=title,
        sprint=sprint,
        user_story=story,
        governance_level=governance,
        template=template
    )

@cli.command()
@click.option('--status', help='Filter by status')
@click.option('--sprint', type=int, help='Filter by sprint')
@click.option('--governance', help='Filter by governance level')
def list(status, sprint, governance):
    """List all ADRs"""
    tool = ADRTOGAFScrumCLI()
    tool.list_adrs(status=status, sprint=sprint, governance_level=governance)

@cli.command()
@click.option('--month', type=int, required=True, help='Month (1-12)')
@click.option('--year', type=int, help='Year (default: current year)')
def review(month, year):
    """Generate Architecture Board review"""
    if year is None:
        year = datetime.now().year

    tool = ADRTOGAFScrumCLI()
    tool.generate_board_review(month, year)

@cli.command()
def metrics():
    """Show architecture metrics"""
    tool = ADRTOGAFScrumCLI()
    tool.show_metrics()

@cli.command()
@click.option('--adr', type=int, help='Check specific ADR')
def check(adr):
    """Check governance compliance"""
    tool = ADRTOGAFScrumCLI()
    tool.check_governance(adr_number=adr)

# Sprint commands
@cli.group()
def sprint():
    """Sprint management commands"""
    pass

@sprint.command()
@click.argument('sprint_number', type=int)
@click.argument('goal')
@click.option('--stories', multiple=True, help='User story IDs')
def plan(sprint_number, goal, stories):
    """Create sprint planning document"""
    tool = ADRTOGAFScrumCLI()
    tool.create_sprint_planning(sprint_number, goal, list(stories))

@sprint.command()
@click.argument('sprint_number', type=int)
def review_sprint(sprint_number):
    """Create sprint review document"""
    tool = ADRTOGAFScrumCLI()
    tool.create_sprint_review(sprint_number)

# TOGAF commands
@cli.group()
def togaf():
    """TOGAF management commands"""
    pass

@togaf.command()
def vision():
    """Create architecture vision"""
    tool = ADRTOGAFScrumCLI()
    tool.create_architecture_vision()

if __name__ == '__main__':
    cli()
```

### Instalación y Uso del CLI

```bash
# Install dependencies
pip install click pyyaml

# Make executable
chmod +x adr-cli.py

# Initialize repository
./adr-cli.py init

# Create ADR
./adr-cli.py new "Authentication Strategy" --sprint 5 --story US-101 --governance tactical

# List ADRs
./adr-cli.py list
./adr-cli.py list --status Accepted
./adr-cli.py list --sprint 5

# Create sprint planning
./adr-cli.py sprint plan 5 "Implement user authentication" --stories US-101 --stories US-102

# Generate board review
./adr-cli.py review --month 12 --year 2025

# Check compliance
./adr-cli.py check
./adr-cli.py check --adr 15

# Show metrics
./adr-cli.py metrics

# Create TOGAF vision
./adr-cli.py togaf vision
```

---

## 7. Casos de Uso Reales

### Caso 1: E-commerce Platform Migration

```python
# ==========================================
# CASO REAL: E-Commerce Platform Migration
# ==========================================

"""
Company: RetailCo
Context: Migrating monolith to microservices
Team: 15 engineers, 3 scrum teams
Timeline: 12 months
Budget: $500K
Compliance: PCI-DSS (payment processing)

Challenge: How to integrate TOGAF governance with Scrum velocity?
"""

class EcommerceMigrationCase:
    """
    Real-world example of ADR + TOGAF + Scrum integration
    for e-commerce platform migration
    """

    def __init__(self):
        self.framework = IntegratedArchitectureFramework()
        self.current_sprint = 0
        self.adrs_created: List[int] = []

    # ========================================
    # QUARTER 1: FOUNDATION
    # ========================================

    def q1_week_1_architecture_vision(self):
        """
        Week 1: Create Architecture Vision (TOGAF Phase A)

        Participants: CTO, Lead Architect, Product Owner
        Duration: 3 days (not 3 months!)
        Output: 5-page vision document
        """
        print("\n" + "="*60)
        print("Q1 WEEK 1: ARCHITECTURE VISION")
        print("="*60 + "\n")

        vision = self.framework.create_architecture_vision(
            business_goals=[
                "Launch new e-commerce platform in 12 months",
                "Support Black Friday: 100K concurrent users",
                "Reduce deployment time from 2 weeks to 1 day",
                "Enable A/B testing for 20% faster iteration"
            ],
            principles=[
                "Cloud-native first (AWS)",
                "Microservices for business capabilities",
                "Event-driven for async operations",
                "Database per service",
                "API-first design",
                "Security by default (PCI-DSS compliant)"
            ],
            constraints={
                "budget": "$500K total",
                "timeline": "12 months to launch",
                "team": "15 engineers (3 scrum teams)",
                "compliance": "PCI-DSS for payments",
                "no_downtime": "Must maintain current site during migration"
            }
        )

        print("📄 Architecture Vision Created:")
        print(f"  Business Goals: {len(vision['business_goals'])}")
        print(f"  Principles: {len(vision['architecture_principles'])}")
        print(f"  Roadmap: {len(vision['roadmap_quarters'])} quarters\n")

        # This created ADR-001: Architecture Vision
        self.adrs_created.append(1)

        return vision

    def q1_week_2_target_architecture(self):
        """
        Week 2: Define Target Architecture (TOGAF Phases B-D)

        Participants: Architecture team + Tech leads from each scrum team
        Duration: 1 week (not 3 months!)
        Output: Architecture Building Blocks + Product Backlog Epics
        """
        print("\n" + "="*60)
        print("Q1 WEEK 2: TARGET ARCHITECTURE")
        print("="*60 + "\n")

        target_arch = self.framework.define_target_architecture(
            current_state={
                "architecture": "Monolithic PHP application",
                "database": "Single MySQL database",
                "deployment": "Manual deployment to on-prem servers",
                "infrastructure": "On-premise data center"
            },
            target_state={
                "architecture": "Microservices (8 core services)",
                "services": [
                    "User Service (authentication, profiles)",
                    "Product Service (catalog, search, inventory)",
                    "Cart Service (shopping cart)",
                    "Order Service (order processing, fulfillment)",
                    "Payment Service (payment processing - PCI compliant)",
                    "Notification Service (email, SMS)",
                    "Analytics Service (tracking, reporting)",
                    "Search Service (Elasticsearch)"
                ],
                "databases": "PostgreSQL per service + Redis cache + Elasticsearch",
                "deployment": "Kubernetes (EKS) with CI/CD (GitHub Actions + ArgoCD)",
                "infrastructure": "AWS multi-region"
            },
            gap_analysis=[
                "No cloud infrastructure → Need AWS account, VPC, EKS setup",
                "No microservices → Need to extract services from monolith",
                "Single database → Need to decompose data",
                "No CI/CD → Need to build pipeline",
                "No event system → Need Kafka for async communication",
                "No PCI compliance → Need tokenization for payments"
            ]
        )

        print("🏗️  Target Architecture Defined:")
        print(f"  Services: {len(target_arch['target_state']['services'])}")
        print(f"  Gaps: {len(target_arch['gaps'])}")
        print(f"  Epics Created: {len(target_arch['product_backlog'])}\n")

        # Convert to product backlog
        product_backlog = target_arch['product_backlog']

        print("📋 Product Backlog (Top 5 Epics):")
        for epic in product_backlog[:5]:
            print(f"  {epic['id']}: {epic['title']} ({epic['estimated_sprints']} sprints)")

        return target_arch

    # ========================================
    # SPRINT 1: Infrastructure Foundation
    # ========================================

    def sprint_1_planning(self):
        """
        Sprint 1 Planning: Infrastructure Foundation

        Goal: Setup cloud infrastructure and CI/CD
        Duration: 2 weeks
        Team: DevOps team (5 engineers)
        """
        self.current_sprint = 1

        print("\n" + "="*60)
        print("SPRINT 1 PLANNING")
        print("="*60 + "\n")

        user_stories = [
            {
                "id": "US-001",
                "title": "As DevOps, I want to create AWS infrastructure",
                "points": 8,
                "description": "Setup VPC, subnets, security groups, EKS cluster",
                "acceptance_criteria": [
                    "EKS cluster running in us-east-1",
                    "kubectl access configured",
                    "Infrastructure as Code (Terraform)"
                ]
            },
            {
                "id": "US-002",
                "title": "As Developer, I want CI/CD pipeline for automated deployments",
                "points": 5,
                "description": "GitHub Actions for build, ArgoCD for deployment",
                "acceptance_criteria": [
                    "PR triggers build and tests",
                    "Merge to main auto-deploys to staging",
                    "Manual approval for production"
                ]
            },
            {
                "id": "US-003",
                "title": "As Developer, I want observability stack for monitoring",
                "points": 5,
                "description": "Prometheus, Grafana, Jaeger for metrics, logs, traces",
                "acceptance_criteria": [
                    "Prometheus collecting metrics",
                    "Grafana dashboards for key metrics",
                    "Jaeger for distributed tracing"
                ]
            }
        ]

        planning = self.framework.sprint_planning(
            sprint_number=1,
            user_stories=user_stories
        )

        print("📋 Sprint 1 Commitment:")
        print(f"  Stories: {len(planning['user_stories'])}")
        print(f"  Total Points: {sum(s['points'] for s in user_stories)}")
        print(f"  ADRs to Create: {len(planning['adr_drafts'])}\n")

        # Architecture decisions identified:
        # - ADR-002: Cloud Provider Selection (AWS vs GCP vs Azure)
        # - ADR-003: Kubernetes Distribution (EKS vs GKE vs AKS)
        # - ADR-004: CI/CD Tool Selection (GitHub Actions vs GitLab vs Jenkins)
        # - ADR-005: Observability Stack (Prometheus vs Datadog vs New Relic)

        print("🏗️  Architecture Decisions Needed:")
        for adr in planning['adr_drafts']:
            print(f"  ADR-{adr.adr_number}: {adr.title}")
            self.adrs_created.append(adr.adr_number)

        return planning

    def sprint_1_day_2_spike_cloud_provider(self):
        """
        Sprint 1 Day 2-3: Spike - Research Cloud Provider

        Task: Evaluate AWS vs GCP vs Azure
        Owner: DevOps Lead
        Timebox: 8 hours
        """
        print("\n" + "="*60)
        print("SPRINT 1 DAY 2-3: CLOUD PROVIDER SPIKE")
        print("="*60 + "\n")

        # Research findings
        findings = {
            "options": [
                {
                    "name": "AWS EKS",
                    "pros": [
                        "Team has most AWS experience",
                        "Best ecosystem (RDS, ElastiCache, MSK all integrated)",
                        "Excellent CLI tooling (eksctl, AWS CDK)",
                        "Good documentation"
                    ],
                    "cons": [
                        "Slightly more expensive than GCP",
                        "EKS control plane costs $73/month per cluster"
                    ],
                    "cost": "$2,500/month (estimate for our scale)",
                    "complexity": "Medium",
                    "risk": "Low (team expertise)"
                },
                {
                    "name": "GCP GKE",
                    "pros": [
                        "Cheapest option",
                        "Best Kubernetes integration (Google created K8s)",
                        "Free control plane for zonal clusters",
                        "Excellent for data/ML workloads"
                    ],
                    "cons": [
                        "Team has less GCP experience",
                        "Smaller ecosystem than AWS",
                        "Learning curve for team"
                    ],
                    "cost": "$2,000/month (estimate)",
                    "complexity": "Medium",
                    "risk": "Medium (learning curve)"
                },
                {
                    "name": "Azure AKS",
                    "pros": [
                        "Free control plane",
                        "Good if we used Microsoft stack (we don't)",
                        "Good enterprise support"
                    ],
                    "cons": [
                        "Team has no Azure experience",
                        "Smaller ecosystem for our needs",
                        "Documentation not as comprehensive"
                    ],
                    "cost": "$2,200/month (estimate)",
                    "complexity": "High",
                    "risk": "High (no expertise)"
                }
            ],
            "recommendation": {
                "option": "AWS EKS",
                "reason": """
                Despite being slightly more expensive, AWS is the best choice because:
                1. Team expertise (4/5 engineers have AWS experience)
                2. Integrated ecosystem (RDS for PostgreSQL, ElastiCache for Redis, MSK for Kafka)
                3. Faster time to market (no learning curve)
                4. Better support for PCI-DSS compliance
                5. Cost difference is only $500/month, but saves 2-3 weeks of learning time

                ROI: $500/month * 12 = $6K/year extra cost
                     vs 2 weeks delay = $50K+ in delayed revenue

                Clear winner: AWS EKS
                """
            }
        }

        print("🔬 Cloud Provider Research Complete\n")
        print("Options Evaluated:")
        for opt in findings['options']:
            print(f"\n  {opt['name']}:")
            print(f"    Cost: {opt['cost']}")
            print(f"    Risk: {opt['risk']}")
            print(f"    Complexity: {opt['complexity']}")

        print(f"\n💡 Recommendation: {findings['recommendation']['option']}")
        print(f"   Reason: {findings['recommendation']['reason'][:100]}...")

        # Update ADR-002 with findings
        adr_002 = self.framework.adrs[2]
        adr_002.options_considered = findings['options']
        adr_002.status = "Proposed"

        return findings

    def sprint_1_day_4_team_decision(self):
        """
        Sprint 1 Day 4: Team Decision Meeting

        Agenda: Review cloud provider research, make decision
        Participants: DevOps team + Lead Architect
        Duration: 1 hour
        """
        print("\n" + "="*60)
        print("SPRINT 1 DAY 4: DECISION MEETING")
        print("="*60 + "\n")

        # Team discussion
        discussion = {
            "comments": [
                {
                    "person": "DevOps Lead",
                    "comment": "AWS makes sense - we all know it well"
                },
                {
                    "person": "Engineer 1",
                    "comment": "Agree, but we should use Terraform not CloudFormation for multi-cloud flexibility"
                },
                {
                    "person": "Lead Architect",
                    "comment": "Good point - Terraform IaC future-proofs us if we need multi-cloud later"
                },
                {
                    "person": "Security Engineer",
                    "comment": "AWS has good PCI-DSS compliance documentation, that's important for payments"
                }
            ],
            "decision": """
            Use AWS EKS for Kubernetes infrastructure.
            - Region: us-east-1 (primary), us-west-2 (DR)
            - EKS version: 1.28
            - Node groups: t3.medium (2-10 nodes, auto-scaling)
            - Infrastructure as Code: Terraform
            - Cost: ~$2,500/month
            """,
            "rationale": """
            AWS EKS chosen for:
            1. Team expertise → faster delivery
            2. Integrated ecosystem → easier integrations
            3. PCI-DSS support → required for payments
            4. Terraform IaC → multi-cloud flexibility later if needed

            Cost $500/month more than GCP, but saves 2-3 weeks of learning time
            and reduces risk. ROI positive.
            """,
            "consequences": {
                "positive": [
                    "Team can start immediately (no learning curve)",
                    "Integrated services (RDS, ElastiCache, MSK)",
                    "Faster time to market",
                    "Good PCI-DSS compliance support"
                ],
                "negative": [
                    "Higher cost than GCP ($500/month = $6K/year)",
                    "EKS control plane costs $73/month per cluster",
                    "Some AWS lock-in (mitigated by Terraform)"
                ],
                "risks": [
                    {
                        "risk": "AWS pricing increases",
                        "mitigation": "Use Terraform - can migrate to GCP if needed",
                        "probability": "Low",
                        "impact": "Medium"
                    },
                    {
                        "risk": "EKS outages",
                        "mitigation": "Multi-AZ deployment + DR in us-west-2",
                        "probability": "Low",
                        "impact": "High"
                    }
                ]
            }
        }

        print("🎯 Decision Made: AWS EKS")
        print(f"\n💬 Team Discussion ({len(discussion['comments'])} comments):")
        for comment in discussion['comments']:
            print(f"  {comment['person']}: {comment['comment']}")

        # Update ADR-002
        adr_002 = self.framework.adrs[2]
        adr_002.decision = discussion['decision']
        adr_002.status = "Accepted"
        adr_002.decision_date = datetime.now()
        adr_002.consequences = discussion['consequences']

        print(f"\n✅ ADR-002 Updated: Status = Accepted")

        # Check if needs Architecture Board approval
        if adr_002.requires_board_approval:
            print(f"⚠️  Requires Architecture Board approval (next monthly review)")
            adr_002.status = "Pending Board Approval"

        return discussion

    def sprint_1_review(self):
        """
        Sprint 1 Review: Demo infrastructure + Present ADRs

        Stakeholders: Product Owner, CTO, Architecture Board
        Achievements: AWS infrastructure setup, 4 ADRs finalized
        """
        print("\n" + "="*60)
        print("SPRINT 1 REVIEW")
        print("="*60 + "\n")

        print("🎬 Demo: Infrastructure")
        print("  ✅ EKS cluster running in us-east-1")
        print("  ✅ CI/CD pipeline (GitHub Actions + ArgoCD)")
        print("  ✅ Observability stack (Prometheus + Grafana)\n")

        print("📄 Architecture Decisions Made:")
        sprint_1_adrs = [2, 3, 4, 5]  # ADRs created in sprint 1

        for adr_num in sprint_1_adrs:
            adr = self.framework.adrs[adr_num]
            print(f"  ADR-{adr.adr_number:04d}: {adr.title}")
            print(f"    Decision: {adr.decision[:60]}...")
            print(f"    Status: {adr.status}")
            print()

        print("📊 Sprint Metrics:")
        print("  Velocity: 18/18 points (100%)")
        print("  ADRs Created: 4")
        print("  ADRs Accepted: 4")
        print("  Infrastructure: ✅ Complete\n")

        print("🚀 Next Sprint Preview:")
        print("  Goal: Extract User Service from monolith")
        print("  Expected ADRs:")
        print("    - Database strategy (database per service?)")
        print("    - Authentication approach (JWT vs OAuth)")
        print("    - API design (REST vs GraphQL)")

    # ========================================
    # MONTHLY: ARCHITECTURE BOARD REVIEW
    # ========================================

    def month_1_architecture_board_review(self):
        """
        Month 1: Architecture Board Review

        Review Sprint 1-2 ADRs (8 ADRs total)
        Check compliance with architecture principles
        Approve/reject strategic decisions
        """
        print("\n" + "="*60)
        print("MONTH 1: ARCHITECTURE BOARD REVIEW")
        print("="*60 + "\n")

        board_review = self.framework.architecture_board_review(month=1)

        print("📋 Architecture Board Meeting")
        print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"  Attendees: CTO, Lead Architect, Security Lead\n")

        print(f"📊 ADRs Reviewed: {board_review['adrs_reviewed']}")
        print(f"  Approved: {len(board_review['approvals'])}")
        print(f"  Concerns: {len(board_review['concerns'])}\n")

        if board_review['approvals']:
            print("✅ Approved ADRs:")
            for approval in board_review['approvals']:
                print(f"  - {approval['adr']}: {approval['title']}")

        if board_review['concerns']:
            print("\n⚠️  ADRs with Concerns:")
            for concern in board_review['concerns']:
                print(f"  - {concern['adr']}")
                for issue in concern['issues']:
                    print(f"    Issue: {issue}")
                print(f"    Recommendation: {concern['recommendation']}")

        print("\n💡 Strategic Recommendations:")
        print("  1. Good pace of decision-making (8 ADRs in 2 sprints)")
        print("  2. All decisions align with cloud-native principle ✅")
        print("  3. Recommend: Create security review process for future ADRs")

    # ========================================
    # SUMMARY
    # ========================================

    def summary_q1(self):
        """Quarter 1 Summary: Foundation Complete"""

        print("\n" + "="*60)
        print("QUARTER 1 SUMMARY")
        print("="*60 + "\n")

        print("✅ Achievements:")
        print("  - Architecture Vision created (Week 1)")
        print("  - Target Architecture defined (Week 2)")
        print("  - Infrastructure setup complete (Sprints 1-2)")
        print("  - User Service extracted (Sprints 3-4)")
        print(f"  - Total ADRs: {len(self.adrs_created)}")
        print("  - Architecture Board reviews: 2")
        print("  - Velocity: 85% average\n")

        print("📊 Q1 Metrics:")
        print("  - ADRs Created: 20")
        print("  - ADRs Accepted: 18")
        print("  - ADRs Pending: 2")
        print("  - Avg Decision Time: 2.3 days")
        print("  - Compliance Rate: 95%\n")

        print("🎯 Q2 Focus:")
        print("  - Extract core services (Product, Cart, Order)")
        print("  - Implement event-driven architecture")
        print("  - Setup Kafka for async communication")
        print("  - Implement PCI-compliant payment processing\n")

        print("💡 Lessons Learned:")
        print("  ✅ ADRs in sprints work well - fast decisions")
        print("  ✅ Monthly board reviews provide needed governance")
        print("  ✅ TOGAF vision kept us aligned with business goals")
        print("  ⚠️  Need earlier security involvement in ADRs")
        print("  ⚠️  Should create ADR template with security checklist")

# ==========================================
# RUN EXAMPLE
# ==========================================

def run_ecommerce_migration_case():
    """Run complete e-commerce migration case"""

    case = EcommerceMigrationCase()

    # Week 1: Vision
    vision = case.q1_week_1_architecture_vision()

    # Week 2: Target Architecture
    target_arch = case.q1_week_2_target_architecture()

    # Sprint 1
    sprint_1_planning = case.sprint_1_planning()
    spike_findings = case.sprint_1_day_2_spike_cloud_provider()
    decision = case.sprint_1_day_4_team_decision()
    case.sprint_1_review()

    # Monthly review
    case.month_1_architecture_board_review()

    # Q1 Summary
    case.summary_q1()

if __name__ == "__main__":
    run_ecommerce_migration_case()
```

---

## 8. Implementación Paso a Paso

### Guía de Implementación para tu Organización

```markdown
# Guía de Implementación: ADR + TOGAF + Scrum

## Fase 1: Preparación (Week 1)

### Día 1: Assessment

**Objetivo:** Entender estado actual

**Actividades:**
1. Revisar proceso actual de toma de decisiones
   - ¿Cómo se toman decisiones arquitectónicas hoy?
   - ¿Se documentan? ¿Dónde?
   - ¿Quién las aprueba?

2. Evaluar madurez Scrum
   - ¿Equipos siguiendo Scrum correctamente?
   - ¿Sprint planning, review, retro consistentes?
   - ¿Product backlog bien mantenido?

3. Identificar pain points
   - "No sabemos por qué se tomó esa decisión hace 6 meses"
   - "Decisiones toman demasiado tiempo"
   - "Falta alineación con objetivos de negocio"
   - "Deuda técnica por decisiones no documentadas"

**Output:** Assessment document con findings

### Día 2: Stakeholder Buy-in

**Objetivo:** Get leadership support

**Actividades:**
1. Present case for ADR + TOGAF + Scrum to leadership
   - Problem: Current state pain points
   - Solution: Integrated framework
   - Benefits: Faster decisions, better documentation, governance
   - ROI: Reduced technical debt, faster onboarding

2. Define governance structure
   - Who is on Architecture Board?
   - How often do they meet?
   - What authority do they have?

3. Get commitment
   - Time: Architects need time for framework setup
   - Budget: Tools, training if needed
   - Support: Leadership backing for adoption

**Output:** Executive sponsorship + Governance charter

### Día 3: Team Training

**Objetivo:** Educate teams on framework

**Actividades:**
1. Training session 1: ADRs (2 hours)
   - What are ADRs?
   - When to create them?
   - Template walkthrough
   - Example ADRs

2. Training session 2: TOGAF for Agile (2 hours)
   - TOGAF ADM overview
   - Agile adaptation
   - Architecture Vision exercise
   - Principles definition

3. Training session 3: Integration (2 hours)
   - How ADRs fit in sprint workflow
   - Sprint planning with architecture decisions
   - Architecture Board review process
   - Q&A

**Output:** Trained teams + Training materials

### Día 4-5: Setup

**Objective:** Setup infrastructure

**Activities:**
1. Initialize repository
   ```bash
   # Clone template
   git clone https://github.com/yourorg/adr-togaf-template
   cd adr-togaf-template

   # Initialize
   ./adr-cli.py init

   # Customize config
   vim .adr-config.yaml
   # Edit: project name, team, principles, etc.
   ```

2. Create initial artifacts
   - Architecture vision document
   - Architecture principles
   - ADR template
   - Sprint planning template
   - Board review template

3. Setup automation
   - Install CLI tool
   - Configure CI/CD checks (ADR validation)
   - Setup notifications (Slack/Email for board reviews)

**Output:** Working ADR + TOGAF repository

## Fase 2: Pilot (Sprint 1-3)

### Sprint 1: Pilot with One Team

**Objetivo:** Test framework with single team

**Activities:**

**Sprint Planning:**
1. Identify architecture decisions needed in user stories
2. Create ADR drafts using CLI
   ```bash
   ./adr-cli.py new "Database Selection for User Service" \
     --sprint 1 \
     --story US-101 \
     --governance technical
   ```
3. Plan spikes for research

**During Sprint:**
4. Execute spikes (Days 2-3)
5. Team decision meetings (Day 4)
6. Implementation (Days 5-9)
7. Daily standup: Include ADR progress

**Sprint Review:**
8. Demo working software
9. Present ADRs to stakeholders
10. Collect feedback on ADR process

**Sprint Retro:**
11. Retrospective on ADR process
    - What worked?
    - What didn't?
    - Improvements?

**Metrics to Track:**
- # of ADRs created
- Time to make decision (creation to acceptance)
- Team satisfaction with process
- Stakeholder satisfaction

### Sprint 2-3: Iterate and Improve

**Objetivo:** Refine process based on feedback

**Activities:**
1. Implement improvements from retro
2. Continue ADR creation in sprints
3. Build confidence with process

**Common Issues & Solutions:**

| Issue | Solution |
|-------|----------|
| "ADRs take too much time" | Use lighter template for low-impact decisions |
| "Forget to create ADRs" | Add to Definition of Ready checklist |
| "ADRs not being read" | Present in sprint review, link from code |
| "Decisions still slow" | Reduce governance levels, empower teams more |

### End of Pilot: Review

**Metrics:**
- ADRs created: [N]
- Avg decision time: [X] days
- Team satisfaction: [Y]/5
- Process improvements: [List]

**Decision:** Go/No-go for organization-wide rollout

## Fase 3: Rollout (Month 2-3)

### Month 2: Expand to All Teams

**Objetivo:** Roll out to all scrum teams

**Activities:**

**Week 1: Preparation**
1. Train remaining teams
2. Share pilot learnings
3. Update templates based on pilot feedback

**Week 2-4: Gradual Rollout**
4. Team 2 starts Sprint N
5. Team 3 starts Sprint N+1
6. Team 4 starts Sprint N+2
7. (Stagger start to manage support load)

**Support:**
- Office hours: Architecture team available for questions
- Slack channel: #adr-help
- Pair programming: Architects pair with teams on first ADRs

### Month 3: Architecture Board Cadence

**Objetivo:** Establish governance rhythm

**Activities:**

**Monthly Architecture Board Review:**
1. Schedule: Last Friday of each month, 2 hours
2. Agenda:
   - Review all ADRs from last month
   - Compliance check
   - Strategic recommendations
   - Update roadmap if needed

3. Process:
   ```bash
   # Generate review document
   ./adr-cli.py review --month 3 --year 2025

   # Distribute to board 3 days before meeting
   # During meeting: Complete compliance checks
   # After meeting: Update ADR statuses
   ```

**Quarterly TOGAF Review:**
1. Schedule: Last day of quarter, 4 hours
2. Agenda:
   - Review architecture vision (still aligned?)
   - Review principles (any changes needed?)
   - Review roadmap (on track? Adjustments?)
   - Plan next quarter

## Fase 4: Optimization (Month 4-6)

### Continuous Improvement

**Activities:**

**1. Measure Effectiveness**

Metrics to track:
```python
# Architecture Health Metrics

class ArchitectureHealthMetrics:
    """Track architecture decision effectiveness"""

    def calculate_metrics(self):
        return {
            # Decision Velocity
            "avg_decision_time_days": 2.5,  # Target: <3 days
            "adr_acceptance_rate": 0.92,     # Target: >90%

            # Governance Efficiency
            "board_approval_time_days": 15,  # Target: <30 days
            "compliance_rate": 0.95,         # Target: >90%

            # Team Satisfaction
            "team_satisfaction_score": 4.2,  # Target: >4.0/5
            "usefulness_rating": 4.5,        # Target: >4.0/5

            # Business Impact
            "decisions_reversed": 2,         # Target: <5%
            "technical_debt_incidents": 3,   # Target: decreasing trend

            # Documentation Quality
            "adrs_with_full_context": 0.88,  # Target: >85%
            "adrs_linked_from_code": 0.75,   # Target: >70%
        }
```

**2. Automate Compliance Checks**

```yaml
# .github/workflows/adr-compliance.yml

name: ADR Compliance Check

on:
  pull_request:
    paths:
      - 'docs/architecture/decisions/**.md'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check ADR Format
        run: |
          ./adr-cli.py check --adr $(cat ${{ github.event.pull_request.number }})

      - name: Verify Required Fields
        run: |
          # Check ADR has all required sections
          python scripts/validate-adr.py

      - name: Check Governance Level
        run: |
          # Verify correct approvers for governance level
          python scripts/check-approvers.py
```

**3. Integrate with Development Workflow**

```python
# In code comments, link to ADRs

class UserService:
    """
    User authentication and profile management service

    Architecture Decisions:
    - Authentication: ADR-015 (JWT with refresh tokens)
    - Database: ADR-016 (PostgreSQL with row-level security)
    - Caching: ADR-022 (Redis for session storage)
    """

    def authenticate(self, email: str, password: str):
        """
        Authenticate user with email/password

        See ADR-015 for authentication strategy rationale
        """
        # Implementation follows ADR-015 decision
        pass
```

**4. Build ADR Knowledge Base**

Create searchable ADR database:
```bash
# Generate ADR index
./adr-cli.py list --format json > adrs.json

# Build search index (Elasticsearch)
python scripts/index-adrs.py

# Create web interface for searching ADRs
# Team members can search: "Why did we choose PostgreSQL?"
# Result: ADR-016 with full context
```

## Fase 5: Maturity (Month 7+)

### Advanced Practices

**1. ADR Templates by Domain**

Create specialized templates:
- `template-database.md`: Database selection decisions
- `template-api.md`: API design decisions
- `template-security.md`: Security decisions
- `template-performance.md`: Performance optimization decisions

**2. Decision Trees**

```markdown
# Decision Tree: Should I create an ADR?

START → Is this an architecture decision?
         ├─ No → Document in code comments
         └─ Yes → Continue

       → Is it reversible easily?
         ├─ Yes → Governance level: Team
         └─ No → Continue

       → Does it affect multiple services?
         ├─ No → Governance level: Technical
         └─ Yes → Continue

       → Does it cost >$5K/month?
         ├─ No → Governance level: Tactical
         └─ Yes → Governance level: Strategic

       → Create ADR with appropriate governance level
```

**3. ADR Metrics Dashboard**

Build real-time dashboard:
- ADRs by status (pie chart)
- Decision velocity trend (line chart)
- Compliance rate over time (line chart)
- Top decision makers (bar chart)
- Recent ADRs (table)

**4. Retrospective ADRs**

Periodically review past decisions:
```bash
# Every 6 months: Review all ADRs from 12+ months ago

./adr-cli.py list --older-than 12-months

# For each ADR:
# - Is decision still valid?
# - What did we learn?
# - Would we decide differently now?
# - Should ADR be superseded?
```

## Success Criteria

Your implementation is successful when:

✅ **Adoption:**
- [ ] 100% of teams creating ADRs in sprints
- [ ] <5% of architecture decisions undocumented
- [ ] Architecture Board meeting monthly

✅ **Velocity:**
- [ ] Avg decision time <3 days
- [ ] Board review time <30 days
- [ ] 95%+ ADR acceptance rate

✅ **Quality:**
- [ ] 90%+ compliance with principles
- [ ] 85%+ ADRs with full context
- [ ] <5% decisions reversed

✅ **Satisfaction:**
- [ ] Team satisfaction >4.0/5
- [ ] Stakeholder satisfaction >4.0/5
- [ ] New team members find ADRs useful for onboarding

✅ **Business Impact:**
- [ ] Technical debt decreasing
- [ ] Faster decision-making
- [ ] Better alignment with business goals
- [ ] Reduced "we don't know why" moments

## Troubleshooting

### Common Problems & Solutions

**Problem: Teams forget to create ADRs**

Solutions:
1. Add to Definition of Ready:
   - "Architecture decisions identified and ADR drafts created"
2. Sprint planning checklist:
   - [ ] Review user stories for architecture decisions
   - [ ] Create ADR drafts for identified decisions
3. Automated reminder:
   - Bot comments on large PRs: "Did this require an ADR?"

**Problem: ADRs taking too long**

Solutions:
1. Use lighter templates for low-impact decisions
2. Set timeboxes: "Decision must be made by Day 4"
3. Reduce bureaucracy: Team-level decisions don't need approval
4. Parallel processing: Research options in parallel

**Problem: ADRs not being read/used**

Solutions:
1. Link ADRs from code (comments, PRs)
2. Present ADRs in sprint reviews
3. Include in onboarding process
4. Search tool: Make ADRs easy to find
5. Dashboard: Visualize ADRs

**Problem: Architecture Board becomes bottleneck**

Solutions:
1. Increase delegation: More decisions at team/technical level
2. Asynchronous approval: Board reviews offline, approves via Slack
3. Parallel reviews: Different board members review different ADRs
4. Standing approval: Pre-approve common patterns

**Problem: Teams feel ADRs are bureaucratic**

Solutions:
1. Show value: "ADR helped new team member understand decision"
2. Reduce overhead: Simpler templates, faster approval
3. Celebrate wins: "ADR prevented us from repeating past mistake"
4. Get feedback: Regular retrospectives on process
5. Flexibility: Allow teams to adapt process to their needs

```

---

## 9. Métricas y KPIs

### Dashboard de Métricas Arquitectónicas

```python
# ==========================================
# ARCHITECTURE METRICS & KPIs
# ==========================================

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta
import statistics

@dataclass
class ArchitectureMetrics:
    """Métricas para medir efectividad de ADR + TOGAF + Scrum"""

    # Decision Velocity Metrics
    total_adrs: int
    adrs_by_status: Dict[str, int]
    avg_decision_time_days: float
    decision_time_trend: List[float]  # Last 6 months

    # Governance Metrics
    board_reviews_completed: int
    compliance_rate: float  # % ADRs compliant with principles
    board_approval_time_days: float
    escalation_rate: float  # % ADRs requiring board approval

    # Team Satisfaction Metrics
    team_satisfaction_score: float  # 1-5
    perceived_usefulness: float  # 1-5
    time_burden_rating: float  # 1-5 (lower is better)

    # Quality Metrics
    adrs_with_full_context: float  # %
    adrs_linked_from_code: float  # %
    decisions_reversed: int
    decisions_superseded: int

    # Business Impact Metrics
    technical_debt_incidents: int
    onboarding_time_reduction: float  # %
    decision_clarity_incidents: int  # "We don't know why" moments

    # Sprint Integration Metrics
    adrs_per_sprint: float  # Average
    sprints_with_adrs: float  # %
    architecture_stories_completion: float  # %

class MetricsDashboard:
    """
    Dashboard para visualizar métricas arquitectónicas

    Genera reportes y visualizaciones del estado de ADRs,
    compliance con TOGAF, y efectividad de integración con Scrum
    """

    def __init__(self, framework: IntegratedArchitectureFramework):
        self.framework = framework
        self.metrics_history: List[Dict] = []

    def calculate_current_metrics(self) -> ArchitectureMetrics:
        """Calcula métricas actuales"""

        adrs = list(self.framework.adrs.values())

        # Decision Velocity
        total_adrs = len(adrs)

        adrs_by_status = {}
        for adr in adrs:
            status = adr.status
            adrs_by_status[status] = adrs_by_status.get(status, 0) + 1

        # Calculate avg decision time
        decision_times = []
        for adr in adrs:
            if adr.decision_date and adr.created_date:
                delta = adr.decision_date - adr.created_date
                decision_times.append(delta.days + delta.seconds / 86400)

        avg_decision_time = statistics.mean(decision_times) if decision_times else 0

        # Governance
        strategic_tactical = [
            adr for adr in adrs
            if adr.governance_level in [GovernanceLevel.STRATEGIC, GovernanceLevel.TACTICAL]
        ]
        escalation_rate = len(strategic_tactical) / total_adrs if total_adrs > 0 else 0

        # Compliance
        compliant_adrs = [
            adr for adr in adrs
            if self._is_compliant(adr)
        ]
        compliance_rate = len(compliant_adrs) / total_adrs if total_adrs > 0 else 0

        # Quality
        adrs_with_context = [
            adr for adr in adrs
            if len(adr.context) > 100  # Has substantial context
        ]
        context_rate = len(adrs_with_context) / total_adrs if total_adrs > 0 else 0

        # Sprint integration
        sprints_with_adrs = len(set(adr.sprint_number for adr in adrs if adr.sprint_number))
        total_sprints = max((adr.sprint_number for adr in adrs if adr.sprint_number), default=0)
        sprint_integration = sprints_with_adrs / total_sprints if total_sprints > 0 else 0

        adrs_per_sprint = total_adrs / total_sprints if total_sprints > 0 else 0

        # Reversals
        decisions_reversed = len([adr for adr in adrs if adr.status == "Rejected"])
        decisions_superseded = len([adr for adr in adrs if adr.status == "Superseded"])

        metrics = ArchitectureMetrics(
            total_adrs=total_adrs,
            adrs_by_status=adrs_by_status,
            avg_decision_time_days=avg_decision_time,
            decision_time_trend=[],  # Would track over time
            board_reviews_completed=0,  # Would track from governance
            compliance_rate=compliance_rate,
            board_approval_time_days=15.0,  # Placeholder
            escalation_rate=escalation_rate,
            team_satisfaction_score=4.2,  # Would survey teams
            perceived_usefulness=4.5,  # Would survey teams
            time_burden_rating=2.8,  # Would survey teams
            adrs_with_full_context=context_rate,
            adrs_linked_from_code=0.75,  # Would scan codebase
            decisions_reversed=decisions_reversed,
            decisions_superseded=decisions_superseded,
            technical_debt_incidents=0,  # Would track separately
            onboarding_time_reduction=0.30,  # 30% faster onboarding
            decision_clarity_incidents=0,  # Would track separately
            adrs_per_sprint=adrs_per_sprint,
            sprints_with_adrs=sprint_integration,
            architecture_stories_completion=0.85  # 85% completion rate
        )

        # Store in history
        self.metrics_history.append({
            'date': datetime.now(),
            'metrics': metrics
        })

        return metrics

    def generate_report(self, metrics: ArchitectureMetrics) -> str:
        """Generate text report"""

        report = f"""
{'='*70}
ARCHITECTURE METRICS REPORT
{'='*70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 DECISION VELOCITY
{'-'*70}
Total ADRs:                     {metrics.total_adrs}
Avg Decision Time:              {metrics.avg_decision_time_days:.1f} days
Target: <3 days                 {'✅ GOOD' if metrics.avg_decision_time_days < 3 else '⚠️ NEEDS IMPROVEMENT'}

ADRs by Status:
"""

        for status, count in sorted(metrics.adrs_by_status.items()):
            percentage = (count / metrics.total_adrs * 100) if metrics.total_adrs > 0 else 0
            report += f"  {status:20s}: {count:3d} ({percentage:5.1f}%)\n"

        report += f"""
⚖️  GOVERNANCE
{'-'*70}
Compliance Rate:                {metrics.compliance_rate*100:.1f}%
Target: >90%                    {'✅ GOOD' if metrics.compliance_rate > 0.9 else '⚠️ NEEDS IMPROVEMENT'}

Escalation Rate:                {metrics.escalation_rate*100:.1f}%
Board Approval Time:            {metrics.board_approval_time_days:.1f} days
Target: <30 days                {'✅ GOOD' if metrics.board_approval_time_days < 30 else '⚠️ SLOW'}

📈 QUALITY
{'-'*70}
ADRs with Full Context:         {metrics.adrs_with_full_context*100:.1f}%
Target: >85%                    {'✅ GOOD' if metrics.adrs_with_full_context > 0.85 else '⚠️ NEEDS IMPROVEMENT'}

ADRs Linked from Code:          {metrics.adrs_linked_from_code*100:.1f}%
Target: >70%                    {'✅ GOOD' if metrics.adrs_linked_from_code > 0.7 else '⚠️ NEEDS IMPROVEMENT'}

Decisions Reversed:             {metrics.decisions_reversed}
Decisions Superseded:           {metrics.decisions_superseded}
Target: <5% reversal rate       {'✅ GOOD' if metrics.decisions_reversed < metrics.total_adrs * 0.05 else '⚠️ HIGH'}

👥 TEAM SATISFACTION
{'-'*70}
Team Satisfaction:              {metrics.team_satisfaction_score:.1f}/5.0
Target: >4.0                    {'✅ GOOD' if metrics.team_satisfaction_score > 4.0 else '⚠️ NEEDS IMPROVEMENT'}

Perceived Usefulness:           {metrics.perceived_usefulness:.1f}/5.0
Time Burden:                    {metrics.time_burden_rating:.1f}/5.0 (lower is better)
Target: <3.0                    {'✅ GOOD' if metrics.time_burden_rating < 3.0 else '⚠️ TOO BURDENSOME'}

🚀 SPRINT INTEGRATION
{'-'*70}
ADRs per Sprint:                {metrics.adrs_per_sprint:.1f}
Sprints with ADRs:              {metrics.sprints_with_adrs*100:.1f}%
Target: >80%                    {'✅ GOOD' if metrics.sprints_with_adrs > 0.8 else '⚠️ LOW INTEGRATION'}

Architecture Stories Complete:  {metrics.architecture_stories_completion*100:.1f}%

💼 BUSINESS IMPACT
{'-'*70}
Technical Debt Incidents:       {metrics.technical_debt_incidents}
Onboarding Time Reduction:      {metrics.onboarding_time_reduction*100:.0f}%
"Why?" Incidents:               {metrics.decision_clarity_incidents}

{'='*70}

💡 RECOMMENDATIONS:
"""

        # Generate recommendations based on metrics
        recommendations = self._generate_recommendations(metrics)
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"

        report += f"\n{'='*70}\n"

        return report

    def _generate_recommendations(self, metrics: ArchitectureMetrics) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []

        # Decision velocity
        if metrics.avg_decision_time_days > 3:
            recommendations.append(
                f"⚠️ Decision time is {metrics.avg_decision_time_days:.1f} days (target: <3). "
                f"Consider: earlier decision meetings, reduce approval layers, timeboxing decisions."
            )

        # Compliance
        if metrics.compliance_rate < 0.9:
            recommendations.append(
                f"⚠️ Compliance rate is {metrics.compliance_rate*100:.0f}% (target: >90%). "
                f"Consider: ADR template improvements, automated compliance checks, training."
            )

        # Context quality
        if metrics.adrs_with_full_context < 0.85:
            recommendations.append(
                f"⚠️ Only {metrics.adrs_with_full_context*100:.0f}% of ADRs have full context (target: >85%). "
                f"Consider: better templates, examples, review process."
            )

        # Team satisfaction
        if metrics.team_satisfaction_score < 4.0:
            recommendations.append(
                f"⚠️ Team satisfaction is {metrics.team_satisfaction_score:.1f}/5.0 (target: >4.0). "
                f"Consider: process improvements, reduce bureaucracy, show value."
            )

        # Time burden
        if metrics.time_burden_rating > 3.0:
            recommendations.append(
                f"⚠️ Time burden rated {metrics.time_burden_rating:.1f}/5.0 (target: <3.0). "
                f"ADRs feel too burdensome. Consider: lighter templates, async approval, tooling."
            )

        # Sprint integration
        if metrics.sprints_with_adrs < 0.8:
            recommendations.append(
                f"⚠️ Only {metrics.sprints_with_adrs*100:.0f}% of sprints have ADRs (target: >80%). "
                f"Consider: sprint planning checklist, automated reminders, Definition of Ready update."
            )

        # Reversals
        reversal_rate = metrics.decisions_reversed / metrics.total_adrs if metrics.total_adrs > 0 else 0
        if reversal_rate > 0.05:
            recommendations.append(
                f"⚠️ {reversal_rate*100:.0f}% of decisions reversed (target: <5%). "
                f"Consider: better research/spikes, involve right stakeholders, prototype before deciding."
            )

        # If all good
        if not recommendations:
            recommendations.append(
                "✅ All metrics are healthy! Keep up the good work. "
                "Continue monitoring and gathering team feedback."
            )

        return recommendations

    def _is_compliant(self, adr: ArchitectureDecision) -> bool:
        """Check if ADR is compliant with standards"""
        # Simplified - real implementation would be more sophisticated
        return (
            adr.status in ["Accepted", "Superseded"] and
            len(adr.context) > 50 and
            len(adr.decision) > 50 and
            len(adr.options_considered) >= 2
        )

# ==========================================
# EXAMPLE USAGE
# ==========================================

def example_metrics_dashboard():
    """Example of metrics dashboard"""

    framework = IntegratedArchitectureFramework()

    # Populate with some example ADRs
    for i in range(1, 21):
        adr = framework._create_adr(
            title=f"Decision {i}",
            togaf_phase=TOGAFPhase.APPLICATION,
            governance_level=GovernanceLevel.TECHNICAL,
            impact=DecisionImpact.MEDIUM,
            context="Example context " * 10,
            decision="Example decision " * 10,
            sprint_number=i // 4 + 1
        )

        # Mark some as accepted
        if i % 3 == 0:
            adr.status = "Accepted"
            adr.decision_date = adr.created_date + timedelta(days=2 + i % 5)
            adr.options_considered = [
                {"name": "Option 1", "pros": [], "cons": []},
                {"name": "Option 2", "pros": [], "cons": []}
            ]

    # Create dashboard
    dashboard = MetricsDashboard(framework)

    # Calculate metrics
    metrics = dashboard.calculate_current_metrics()

    # Generate report
    report = dashboard.generate_report(metrics)

    print(report)

if __name__ == "__main__":
    example_metrics_dashboard()
```

---

## 10. Anti-patterns y Soluciones

### Common Anti-patterns

```markdown
# Anti-Patterns in ADR + TOGAF + Scrum Integration

## Anti-Pattern 1: "ADR for Everything"

**Problem:**
Team creates ADRs for trivial decisions that don't need documentation.

**Example:**
```markdown
# ADR-042: Variable Naming Convention for User Service

Decision: Use camelCase for JavaScript variables
```

**Why it's bad:**
- Wastes time
- Creates noise
- Teams lose faith in process
- Important ADRs buried in trivial ones

**Solution:**
Create decision tree for when to write ADR:

```python
def should_create_adr(decision: str) -> bool:
    """Decision tree for ADR creation"""

    # Rule 1: Is it architectural?
    if not is_architecture_decision(decision):
        return False  # Use code comments instead

    # Rule 2: Is it reversible easily?
    if is_easily_reversible(decision):
        return False  # Just do it, can change later

    # Rule 3: Does it affect multiple teams/services?
    if not affects_multiple_components(decision):
        # Maybe just document in README
        return governance_level(decision) >= GovernanceLevel.TACTICAL

    # Rule 4: Will future developers need context?
    if not needs_historical_context(decision):
        return False

    return True  # Create ADR!
```

**Guidelines:**
- Coding standards → NOT an ADR (use linter config)
- Technology choice → ADR
- Single file refactoring → NOT an ADR (PR description)
- Architecture pattern → ADR

---

## Anti-Pattern 2: "TOGAF Waterfall"

**Problem:**
Using TOGAF as waterfall: 6 months of architecture before coding

**Example:**
```markdown
Quarter 1: Architecture Vision (3 months of docs)
Quarter 2: Target Architecture (3 months of models)
Quarter 3: Migration Planning (3 months of plans)
Quarter 4: Start coding (finally!)
```

**Why it's bad:**
- Slow time to market
- Architecture disconnected from reality
- Team frustration
- Business loses faith

**Solution:**
TOGAF Agile Adaptation:

```python
# WRONG: Waterfall TOGAF
def waterfall_togaf():
    vision = create_vision_100_pages(months=3)  # ❌
    target_arch = create_target_arch_200_pages(months=3)  # ❌
    migration = create_migration_plan_50_pages(months=3)  # ❌
    # 9 months later... start coding
    implement(vision, target_arch, migration)

# RIGHT: Agile TOGAF
def agile_togaf():
    vision = create_vision_lightweight(days=5)  # ✅ 5 pages
    # Immediately start Sprint 1
    for sprint in range(1, 13):
        backlog = refine_backlog_from_vision(vision)
        implement_sprint(backlog)
        # Evolve vision based on learnings
        vision = update_vision(vision, learnings)
```

**Guidelines:**
- Vision: 1 week, 5 pages
- Target Architecture: 2 weeks, 20 pages
- Start coding: Sprint 1 (week 3!)
- Evolve architecture each sprint

---

## Anti-Pattern 3: "Architecture Board Bottleneck"

**Problem:**
All decisions require Architecture Board approval → slow

**Example:**
```markdown
Team: "We want to use Redis for caching"
Process: Create ADR → Wait 3 weeks for monthly board meeting →
         Board requests changes → Update ADR → Wait 3 more weeks →
         Finally approved after 6 weeks
```

**Why it's bad:**
- Kills team velocity
- Frustrates teams
- Decisions made anyway (without approval)
- Board becomes rubber stamp

**Solution:**
Governance levels with delegation:

```python
class GovernanceLevelDelegation:
    """
    Delegate decisions to appropriate level
    Only escalate what truly needs Board approval
    """

    LEVELS = {
        "team": {
            "approvers": ["Tech Lead"],
            "max_cost": "$1K/month",
            "examples": [
                "Caching strategy (Redis vs Memcached)",
                "Logging library",
                "Testing framework"
            ],
            "approval_time": "Same day"
        },
        "technical": {
            "approvers": ["Lead Architect"],
            "max_cost": "$5K/month",
            "examples": [
                "Database for single service",
                "API design pattern",
                "Monitoring tool"
            ],
            "approval_time": "1-2 days (async)"
        },
        "tactical": {
            "approvers": ["Architecture Council"],
            "max_cost": "$10K/month",
            "examples": [
                "New microservice creation",
                "Event-driven architecture adoption",
                "Service mesh implementation"
            ],
            "approval_time": "1 week"
        },
        "strategic": {
            "approvers": ["Architecture Board + CTO"],
            "max_cost": "Unlimited",
            "examples": [
                "Cloud provider migration",
                "Monolith to microservices",
                "Compliance framework (PCI-DSS)"
            ],
            "approval_time": "Monthly board meeting"
        }
    }
```

**Guidelines:**
- 80% decisions at Team/Technical level (fast)
- 15% decisions at Tactical level (1 week)
- 5% decisions at Strategic level (monthly)

---

## Anti-Pattern 4: "ADR Shelf-ware"

**Problem:**
ADRs created but never read or used

**Example:**
```markdown
# Team creates 50 ADRs
# New team member joins
# Asks: "Why did we choose PostgreSQL?"
# Team: "I don't know, check the ADRs... somewhere..."
# New member: "Where are they? How do I search?"
# Team: "Uh... Git? Confluence? Not sure..."
```

**Why it's bad:**
- ADRs provide no value if not accessible
- Defeats entire purpose
- Time wasted creating them

**Solution:**
Make ADRs searchable and linked:

```python
class ADRDiscoverability:
    """Make ADRs easy to find and use"""

    def make_discoverable(self):
        # 1. Centralized index
        self.create_adr_index()

        # 2. Search tool
        self.setup_search_tool()

        # 3. Link from code
        self.link_from_code()

        # 4. Link from docs
        self.link_from_docs()

        # 5. Present in meetings
        self.present_in_sprint_reviews()

    def link_from_code(self):
        """Link ADRs from code comments"""

        # In database.py
        """
        Database connection using PostgreSQL

        Why PostgreSQL? See ADR-016:
        docs/architecture/decisions/ADR-0016-database-selection.md

        Key decision points:
        - ACID compliance needed
        - JSON support for flexibility
        - Team expertise
        - Cost-effective at our scale
        """

    def create_search_tool(self):
        """CLI tool to search ADRs"""

        # $ adr search "database"
        # Results:
        # ADR-0016: Database Selection for User Service
        # ADR-0023: Database Migration Strategy
        # ADR-0031: Database Backup and Recovery

        # $ adr search "postgresql"
        # ADR-0016: Database Selection for User Service
        #   Decision: Use PostgreSQL for relational data
        #   Rationale: ACID compliance, JSON support, team expertise

    def onboarding_checklist(self):
        """Include ADRs in onboarding"""

        checklist = """
        New Team Member Onboarding:
        Week 1:
        - [ ] Read Architecture Vision
        - [ ] Read top 10 ADRs:
          - [ ] ADR-001: Architecture Vision
          - [ ] ADR-002: Cloud Provider (AWS)
          - [ ] ADR-008: Microservices Pattern
          - [ ] ADR-015: Authentication Strategy
          - [ ] ADR-016: Database Selection
          ...
        """
```

**Guidelines:**
- Centralized location (docs/architecture/decisions/)
- Search tool (CLI or web interface)
- Link from code
- Include in onboarding
- Present in sprint reviews

---

## Anti-Pattern 5: "Perfect is the Enemy of Good"

**Problem:**
Spending too much time on ADR perfection

**Example:**
```markdown
Day 1: Create ADR draft
Day 2-5: Research every possible option (20 options!)
Day 6-8: Detailed cost analysis for each option
Day 9-10: Write 10-page ADR with exhaustive analysis
Day 11: Team meeting to review (no time to read it all)
Day 12: Revisions
...
Day 20: Still not decided!
```

**Why it's bad:**
- Analysis paralysis
- Slow decision-making
- Team frustration
- Sprint goals missed

**Solution:**
Timebox decisions:

```python
class TimeboxedDecisionMaking:
    """
    Make good-enough decisions fast

    Perfect decision in 3 weeks < Good decision in 3 days
    """

    def sprint_decision_timeline(self):
        """Timeline for decisions in sprint"""

        return {
            "Day 1 (Sprint Planning)": {
                "activity": "Identify decision needed",
                "output": "ADR draft created",
                "time": "30 minutes"
            },
            "Day 2-3 (Spike)": {
                "activity": "Research top 3 options (not 20!)",
                "output": "Comparison table",
                "time": "4 hours (timeboxed!)",
                "rules": [
                    "Max 3 options to evaluate",
                    "Stop at 4 hours even if not perfect",
                    "Focus on key differentiators only"
                ]
            },
            "Day 4 (Decision Meeting)": {
                "activity": "Team discussion and decision",
                "output": "Decision made, ADR updated",
                "time": "1 hour",
                "rules": [
                    "Must decide by end of meeting",
                    "Use voting if consensus fails",
                    "Defer to subject matter expert if needed"
                ]
            },
            "Day 5-9 (Implementation)": {
                "activity": "Implement the decision",
                "output": "Working software",
                "time": "Rest of sprint"
            }
        }

    def decision_quality_vs_time(self):
        """
        Decision quality doesn't improve linearly with time

        Time vs Quality:
        - 1 hour research: 60% confidence
        - 4 hours research: 85% confidence ← sweet spot!
        - 40 hours research: 90% confidence (not worth it!)
        """

        return "Aim for 80-85% confidence, not 100%"

    def rules_for_good_enough_decisions(self):
        """Guidelines for fast, good-enough decisions"""

        return [
            "1. Timebox research (4 hours max for most decisions)",
            "2. Evaluate max 3 options (not 10, not 20)",
            "3. Focus on key differentiators only",
            "4. Make decision by Day 4 of sprint",
            "5. Document decision + rationale (not exhaustive analysis)",
            "6. Iterate if wrong (decisions are reversible!)",
            "7. 'Good enough' decision today > Perfect decision next month"
        ]
```

**Guidelines:**
- Timebox research: 4 hours for most decisions
- Max 3 options to evaluate
- Decide by Day 4 of sprint
- ADRs should be 1-2 pages, not 10 pages
- Aim for 80-85% confidence, not 100%

---

## Anti-Pattern 6: "Decisions Without Context"

**Problem:**
ADRs document decision but not the "why" or context

**Example:**
```markdown
# ADR-025: Use PostgreSQL

## Decision
We will use PostgreSQL for the User Service database.

## Implementation
Install PostgreSQL 14.

[End of ADR]
```

**Why it's bad:**
- No context for future team members
- Can't learn from decision
- Can't evaluate if decision still valid
- Defeats purpose of ADRs

**Solution:**
Rich context in ADRs:

```markdown
# ADR-025: Database Selection for User Service

## Context and Problem

We are extracting User Service from the monolith as part of our
microservices migration (see Architecture Vision ADR-001).

**Current State:**
- Monolith uses single MySQL database (5M users, 2TB data)
- User table has 50 columns (profile, preferences, auth data)
- Frequent joins with orders, products, etc.

**Problem:**
Need to choose database for User Service that will store:
- User profiles (name, email, preferences)
- Authentication data (hashed passwords, MFA secrets)
- User preferences (JSON data, flexible schema)

**Requirements:**
- ACID compliance (critical for auth data)
- JSON support (preferences are flexible)
- 100K concurrent users
- <50ms read latency (p95)
- GDPR compliant (data deletion, encryption)
- Budget: <$500/month
- Team expertise: Important factor

## Options Considered

### Option 1: PostgreSQL
[Full analysis...]

### Option 2: MongoDB
[Full analysis...]

### Option 3: DynamoDB
[Full analysis...]

## Decision

**We chose PostgreSQL**

## Rationale

[Detailed reasoning with business context...]

## Consequences

### Positive
- [Consequences...]

### Negative
- [Trade-offs accepted...]

### Risks
- [Risks and mitigations...]

## Compliance with TOGAF Principles
- [How decision aligns...]

## References
- Spike results: docs/spikes/user-service-database-comparison.md
- Load testing: docs/testing/database-load-test-results.md
- Cost analysis: docs/business/database-cost-comparison.xlsx
```

**Guidelines:**
- Context: Why are we making this decision?
- Problem: What are we solving?
- Options: What did we consider? (min 2-3 options)
- Rationale: Why this option?
- Consequences: Trade-offs we accept
- References: Links to supporting docs

---

## Anti-Pattern 7: "One-Way Decisions"

**Problem:**
Treating all decisions as irreversible

**Example:**
Team: "We chose MongoDB, we can NEVER change it!"
[6 months later, realize PostgreSQL would be better]
Team: "Too late, we're stuck with MongoDB forever!"

**Why it's bad:**
- Fear of decisions
- Analysis paralysis
- Can't adapt to new information
- Stuck with suboptimal choices

**Solution:**
Classify decisions by reversibility:

```python
class DecisionReversibility:
    """
    Not all decisions are equal

    Some are reversible (change database for one service)
    Some are one-way doors (choose programming language for entire platform)
    """

    def classify_decision(self, decision: str) -> str:
        """Classify decision by reversibility"""

        one_way_doors = [
            "Choose cloud provider for entire company",
            "Choose programming language for all services",
            "Commit to vendor with long-term contract",
            "Architectural style (monolith vs microservices)"
        ]

        two_way_doors = [
            "Choose database for single service",
            "Choose caching solution",
            "Choose logging library",
            "Choose testing framework"
        ]

        if decision in one_way_doors:
            return "ONE_WAY_DOOR"  # Hard to reverse, decide carefully
        else:
            return "TWO_WAY_DOOR"  # Can reverse, decide faster

    def decision_approach(self, reversibility: str):
        """How to approach decision based on reversibility"""

        if reversibility == "ONE_WAY_DOOR":
            return {
                "research_time": "1-2 weeks",
                "stakeholders": "Many (CTO, architects, leads)",
                "governance_level": "Strategic",
                "board_approval": True,
                "adr_detail": "Exhaustive",
                "confidence_needed": "95%+"
            }
        else:  # TWO_WAY_DOOR
            return {
                "research_time": "4 hours",
                "stakeholders": "Team + tech lead",
                "governance_level": "Technical",
                "board_approval": False,
                "adr_detail": "Concise",
                "confidence_needed": "80%+",
                "note": "Can change later if needed!"
            }

    def supersede_decision(self, old_adr: int, new_adr: int, reason: str):
        """Mark decision as superseded when circumstances change"""

        # ADR-016: PostgreSQL for User Service
        # Status: Superseded by ADR-087

        # ADR-087: MongoDB for User Service
        # Supersedes: ADR-016
        # Reason: Requirements changed - now need flexible schema for
        #         personalization features. PostgreSQL JSON was getting
        #         unwieldy. Team gained MongoDB expertise. Cost similar.
```

**Guidelines:**
- Classify decisions: One-way vs two-way door
- Two-way doors: Decide fast (4 hours research, 80% confidence)
- One-way doors: Decide carefully (1-2 weeks, 95% confidence)
- It's OK to change decisions when circumstances change!
- Use "Superseded" status when replacing old decision

---

## Summary: Dos and Don'ts

### ✅ DO

1. **DO** create ADRs for architectural decisions
2. **DO** timebox decision-making (4 hours research for most)
3. **DO** delegate to appropriate governance level
4. **DO** make ADRs searchable and discoverable
5. **DO** link ADRs from code
6. **DO** present ADRs in sprint reviews
7. **DO** use lightweight TOGAF (days, not months)
8. **DO** iterate on architecture each sprint
9. **DO** classify decisions by reversibility
10. **DO** supersede decisions when circumstances change

### ❌ DON'T

1. **DON'T** create ADRs for trivial decisions
2. **DON'T** spend weeks on perfect analysis
3. **DON'T** make Architecture Board a bottleneck
4. **DON'T** create ADRs that nobody reads
5. **DON'T** write 10-page ADRs (1-2 pages is fine!)
6. **DON'T** use TOGAF as waterfall (6 months of docs)
7. **DON'T** treat all decisions as irreversible
8. **DON'T** forget to document context and rationale
9. **DON'T** skip sprint integration (ADRs belong in sprints!)
10. **DON'T** ignore team feedback on process
```

---

## Conclusión

Has creado un framework completo para integrar:
- ✅ **ADRs**: Documentación ligera de decisiones
- ✅ **TOGAF**: Governance estratégica
- ✅ **Scrum**: Entrega ágil iterativa

**Beneficios:**
- Decisiones documentadas sin burocracia
- Governance sin sacrificar velocidad
- Alineación arquitectónica con objetivos de negocio
- Onboarding más rápido
- Menos deuda técnica
- Contexto histórico preservado

**Next Steps:**
1. Implementa en proyecto piloto (1-2 sprints)
2. Itera basado en feedback
3. Expande a toda la organización
4. Mide y optimiza continuamente

¡Éxito con tu implementación! 🚀
