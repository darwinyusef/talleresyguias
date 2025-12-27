# ADR + TOGAF + Scrum: Guía de Integración Completa 2026

## Índice
1. [Fundamentos de la Integración](#1-fundamentos)
2. [Architecture Governance Framework](#2-governance-framework)
3. [Sprint Workflow con ADRs](#3-sprint-workflow)
4. [TOGAF ADM Adaptado a Agile](#4-togaf-adm-agile)
5. [Templates y Artefactos](#5-templates)
6. [Herramientas de Automatización](#6-automation)
7. [Casos de Uso Reales](#7-casos-uso)
8. [Implementación Paso a Paso](#8-implementation)
9. [Métricas y KPIs](#9-metrics)
10. [Anti-patterns y Soluciones](#10-antipatterns)

---

## 1. Fundamentos de la Integración

### ❌ PROBLEMA: Frameworks Incompatibles

```python
# MAL - Usar frameworks de forma aislada y contradictoria

# Equipo A: "Usamos TOGAF, necesitamos 6 meses para arquitectura"
togaf_waterfall = {
    "phase_a_vision": "3 meses de documentación",
    "phase_b_business": "2 meses de diagramas",
    "phase_c_data": "2 meses de modelos",
    "phase_d_app": "2 meses de especificaciones",
    "total": "9 meses antes de escribir código"
}

# Equipo B: "Somos Agile, no documentamos nada"
scrum_cowboy_coding = {
    "documentation": "0",
    "architecture_decisions": "Decidimos en el momento",
    "governance": "No hay tiempo para eso",
    "result": "Deuda técnica masiva en 6 meses"
}

# Equipo C: "Escribimos ADRs pero nadie los lee"
adr_shelf_ware = {
    "adrs_written": 50,
    "adrs_reviewed": 2,
    "adrs_followed": 0,
    "value": "Cero - solo burocracia"
}

# ❌ RESULTADO: Caos, deuda técnica, desalineación con negocio
```

### ✅ SOLUCIÓN: Framework Integrado

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# ==========================================
# MODELO DE INTEGRACIÓN ADR + TOGAF + SCRUM
# ==========================================

class GovernanceLevel(Enum):
    """Niveles de governance según tipo de decisión"""
    TEAM = "team"              # Decisión de equipo
    TECHNICAL = "technical"    # Requiere arquitecto técnico
    TACTICAL = "tactical"      # Requiere lead architects
    STRATEGIC = "strategic"    # Requiere Architecture Board

class DecisionImpact(Enum):
    """Impacto de la decisión en el sistema"""
    LOW = "low"           # Cambio reversible, local
    MEDIUM = "medium"     # Afecta múltiples componentes
    HIGH = "high"         # Afecta arquitectura general
    CRITICAL = "critical" # Afecta toda la organización

class TOGAFPhase(Enum):
    """Fases TOGAF ADM"""
    PRELIMINARY = "preliminary"
    VISION = "a_vision"
    BUSINESS = "b_business"
    DATA = "c_data"
    APPLICATION = "d_application"
    TECHNOLOGY = "e_technology"
    OPPORTUNITIES = "f_opportunities"
    MIGRATION = "g_migration"
    GOVERNANCE = "h_governance"

@dataclass
class ArchitectureDecision:
    """ADR integrado con TOGAF y Scrum"""
    adr_number: int
    title: str
    status: str  # Draft, Proposed, Accepted, Rejected, Superseded

    # TOGAF Context
    togaf_phase: TOGAFPhase
    architecture_domain: str  # Business, Data, Application, Technology
    business_driver: str

    # Governance
    governance_level: GovernanceLevel
    impact: DecisionImpact
    requires_board_approval: bool

    # Scrum Context
    sprint_number: Optional[int]
    epic: Optional[str]
    user_stories: List[str]

    # Decision Details
    context: str
    options_considered: List[Dict]
    decision: str
    consequences: Dict[str, List[str]]  # positive, negative, risks

    # Stakeholders
    deciders: List[str]
    consulted: List[str]
    informed: List[str]

    # Metadata
    created_date: datetime
    decision_date: Optional[datetime]
    review_date: Optional[datetime]
    superseded_by: Optional[int]

class IntegratedArchitectureFramework:
    """
    Framework que integra ADR + TOGAF + Scrum

    Niveles de operación:
    - STRATEGIC (Quarterly): TOGAF ADM Phases → Roadmap
    - TACTICAL (Monthly): Architecture Board → Governance
    - OPERATIONAL (Bi-weekly): Scrum Sprints → ADRs
    """

    def __init__(self):
        self.adrs: Dict[int, ArchitectureDecision] = {}
        self.architecture_board: List[str] = []
        self.current_sprint: int = 0
        self.togaf_roadmap: Dict[str, any] = {}

    # ========================================
    # STRATEGIC LEVEL: TOGAF ADM (Quarterly)
    # ========================================

    def create_architecture_vision(
        self,
        business_goals: List[str],
        principles: List[str],
        constraints: Dict[str, str]
    ) -> Dict:
        """
        TOGAF Phase A: Architecture Vision

        Adaptación Agile:
        - En vez de 3 meses de documentación → 2 semanas
        - Output ligero: Vision Statement + Principles + Roadmap
        - Revisión cada trimestre (no cada 3 años)
        """
        vision = {
            "date": datetime.now(),
            "business_goals": business_goals,
            "architecture_principles": principles,
            "constraints": constraints,
            "stakeholders": self._identify_stakeholders(),
            "success_metrics": self._define_success_metrics(),
            "roadmap_quarters": self._create_quarterly_roadmap()
        }

        self.togaf_roadmap = vision

        # Crear ADR para architecture vision
        adr = self._create_adr(
            title="Architecture Vision 2026",
            togaf_phase=TOGAFPhase.VISION,
            governance_level=GovernanceLevel.STRATEGIC,
            impact=DecisionImpact.CRITICAL,
            context=f"Business goals: {', '.join(business_goals)}",
            decision=f"Architecture principles: {', '.join(principles)}"
        )

        return vision

    def define_target_architecture(
        self,
        current_state: Dict,
        target_state: Dict,
        gap_analysis: List[str]
    ) -> Dict:
        """
        TOGAF Phases B-D: Target Architecture

        Adaptación Agile:
        - Architecture en capas (Business, Data, App, Tech)
        - Cada capa = 1 sprint de diseño
        - Output: Architecture Building Blocks (ABBs)
        """
        target_arch = {
            "current_state": current_state,
            "target_state": target_state,
            "gaps": gap_analysis,
            "building_blocks": self._identify_building_blocks(target_state),
            "migration_path": self._create_migration_path(gap_analysis)
        }

        # Convertir architecture a product backlog
        backlog = self._architecture_to_backlog(target_arch)

        return {
            "architecture": target_arch,
            "product_backlog": backlog
        }

    def _architecture_to_backlog(self, architecture: Dict) -> List[Dict]:
        """
        Convierte decisiones arquitectónicas en user stories

        TOGAF → Scrum Bridge
        """
        backlog = []

        for building_block in architecture["building_blocks"]:
            # Cada building block → Epic
            epic = {
                "id": f"EPIC-{len(backlog) + 1}",
                "title": building_block["name"],
                "architecture_component": building_block,
                "user_stories": []
            }

            # Descomponer en user stories
            for capability in building_block["capabilities"]:
                story = {
                    "id": f"US-{len(backlog) + 1}",
                    "title": f"As a {capability['user']}, I want {capability['goal']}",
                    "acceptance_criteria": capability["criteria"],
                    "architecture_decisions_needed": capability.get("decisions", [])
                }
                epic["user_stories"].append(story)

            backlog.append(epic)

        return backlog

    # ========================================
    # TACTICAL LEVEL: Governance (Monthly)
    # ========================================

    def architecture_board_review(self, month: int) -> Dict:
        """
        TOGAF Architecture Board Review (Monthly)

        Revisa:
        1. ADRs del último mes
        2. Compliance con principios
        3. Riesgos arquitectónicos
        4. Aprobaciones pendientes
        """
        # Recopilar ADRs del mes
        month_adrs = [
            adr for adr in self.adrs.values()
            if adr.created_date.month == month
        ]

        review = {
            "date": datetime.now(),
            "adrs_reviewed": len(month_adrs),
            "approvals": [],
            "rejections": [],
            "concerns": [],
            "actions": []
        }

        for adr in month_adrs:
            # Revisar cada ADR
            assessment = self._assess_adr_compliance(adr)

            if assessment["compliant"]:
                review["approvals"].append({
                    "adr": adr.adr_number,
                    "title": adr.title,
                    "status": "Approved"
                })
                adr.status = "Accepted"
            else:
                review["concerns"].append({
                    "adr": adr.adr_number,
                    "issues": assessment["issues"],
                    "recommendation": assessment["recommendation"]
                })

        return review

    def _assess_adr_compliance(self, adr: ArchitectureDecision) -> Dict:
        """Verifica compliance del ADR con principios TOGAF"""
        issues = []

        # Check 1: Alignment con business goals
        if not self._aligns_with_business_goals(adr):
            issues.append("No alignment with business goals")

        # Check 2: Compliance con architecture principles
        if not self._follows_architecture_principles(adr):
            issues.append("Violates architecture principles")

        # Check 3: Risk assessment
        if adr.impact == DecisionImpact.CRITICAL and not adr.consequences.get("risks"):
            issues.append("Missing risk assessment for critical decision")

        # Check 4: Stakeholder involvement
        if adr.governance_level in [GovernanceLevel.TACTICAL, GovernanceLevel.STRATEGIC]:
            if not adr.consulted:
                issues.append("Missing stakeholder consultation")

        return {
            "compliant": len(issues) == 0,
            "issues": issues,
            "recommendation": "Approve" if len(issues) == 0 else "Request changes"
        }

    # ========================================
    # OPERATIONAL LEVEL: Scrum + ADRs (Sprint)
    # ========================================

    def sprint_planning(
        self,
        sprint_number: int,
        user_stories: List[Dict]
    ) -> Dict:
        """
        Sprint Planning con identificación de ADRs

        Proceso:
        1. Product Owner presenta user stories
        2. Team identifica decisiones arquitectónicas necesarias
        3. Crear ADR drafts para cada decisión
        4. Estimar stories + spikes para investigación
        """
        self.current_sprint = sprint_number

        planning = {
            "sprint": sprint_number,
            "user_stories": user_stories,
            "architecture_decisions_needed": [],
            "spikes": [],
            "adr_drafts": []
        }

        # Analizar cada user story para identificar decisiones
        for story in user_stories:
            decisions = self._identify_architecture_decisions(story)

            for decision in decisions:
                # Crear ADR draft
                adr = self._create_adr(
                    title=decision["title"],
                    togaf_phase=TOGAFPhase.APPLICATION,
                    governance_level=self._determine_governance_level(decision),
                    impact=decision["impact"],
                    context=decision["context"],
                    sprint_number=sprint_number,
                    user_stories=[story["id"]]
                )

                planning["adr_drafts"].append(adr)

                # Si requiere investigación, crear spike
                if decision["requires_spike"]:
                    spike = {
                        "title": f"Spike: Research {decision['title']}",
                        "adr": adr.adr_number,
                        "timeboxed": "4 hours",
                        "outcome": "Update ADR with findings"
                    }
                    planning["spikes"].append(spike)

        return planning

    def daily_standup_adr_check(self, day: int) -> List[str]:
        """
        Daily Standup: Check ADR progress

        Questions:
        - What ADRs did we make progress on yesterday?
        - What ADRs are we deciding today?
        - Any blockers on architecture decisions?
        """
        current_sprint_adrs = [
            adr for adr in self.adrs.values()
            if adr.sprint_number == self.current_sprint
        ]

        updates = []
        for adr in current_sprint_adrs:
            if adr.status == "Draft":
                updates.append(f"ADR-{adr.adr_number}: {adr.title} - Still researching")
            elif adr.status == "Proposed":
                updates.append(f"ADR-{adr.adr_number}: {adr.title} - Ready for team review")
            elif adr.status == "Accepted":
                updates.append(f"ADR-{adr.adr_number}: {adr.title} - ✅ Decided, implementing")

        return updates

    def sprint_review_present_adrs(self, sprint_number: int) -> Dict:
        """
        Sprint Review: Present ADRs to stakeholders

        Agenda:
        1. Demo working software
        2. Present architecture decisions made
        3. Get stakeholder feedback
        4. Identify decisions for Architecture Board
        """
        sprint_adrs = [
            adr for adr in self.adrs.values()
            if adr.sprint_number == sprint_number
        ]

        presentation = {
            "sprint": sprint_number,
            "adrs_completed": [],
            "stakeholder_feedback": [],
            "escalations_to_board": []
        }

        for adr in sprint_adrs:
            adr_summary = {
                "number": adr.adr_number,
                "title": adr.title,
                "decision": adr.decision,
                "impact": adr.impact.value,
                "status": adr.status
            }

            presentation["adrs_completed"].append(adr_summary)

            # Si es strategic/critical, escalar a Architecture Board
            if adr.requires_board_approval:
                presentation["escalations_to_board"].append(adr.adr_number)

        return presentation

    def sprint_retrospective_adr_process(self) -> Dict:
        """
        Sprint Retro: Improve ADR process

        Questions:
        - Was our decision-making process effective?
        - Did we involve the right people?
        - Were ADRs helpful or bureaucratic?
        - What can we improve?
        """
        retro = {
            "what_went_well": [],
            "what_to_improve": [],
            "action_items": []
        }

        # Analizar ADRs del sprint
        sprint_adrs = [
            adr for adr in self.adrs.values()
            if adr.sprint_number == self.current_sprint
        ]

        # Metrics
        avg_decision_time = self._calculate_avg_decision_time(sprint_adrs)

        if avg_decision_time < 3:  # days
            retro["what_went_well"].append(
                f"Fast decision making: avg {avg_decision_time} days"
            )
        else:
            retro["what_to_improve"].append(
                f"Slow decisions: avg {avg_decision_time} days - need faster feedback"
            )

        return retro

    # ========================================
    # HELPER METHODS
    # ========================================

    def _create_adr(
        self,
        title: str,
        togaf_phase: TOGAFPhase,
        governance_level: GovernanceLevel,
        impact: DecisionImpact,
        context: str,
        decision: str = "",
        sprint_number: Optional[int] = None,
        user_stories: List[str] = None
    ) -> ArchitectureDecision:
        """Helper para crear ADRs"""
        adr_number = len(self.adrs) + 1

        adr = ArchitectureDecision(
            adr_number=adr_number,
            title=title,
            status="Draft",
            togaf_phase=togaf_phase,
            architecture_domain=self._get_domain_from_phase(togaf_phase),
            business_driver="TBD",
            governance_level=governance_level,
            impact=impact,
            requires_board_approval=governance_level in [
                GovernanceLevel.STRATEGIC,
                GovernanceLevel.TACTICAL
            ],
            sprint_number=sprint_number,
            epic=None,
            user_stories=user_stories or [],
            context=context,
            options_considered=[],
            decision=decision,
            consequences={"positive": [], "negative": [], "risks": []},
            deciders=[],
            consulted=[],
            informed=[],
            created_date=datetime.now(),
            decision_date=None,
            review_date=None,
            superseded_by=None
        )

        self.adrs[adr_number] = adr
        return adr

    def _identify_architecture_decisions(self, user_story: Dict) -> List[Dict]:
        """Identifica decisiones arquitectónicas en user story"""
        decisions = []

        # Heuristics para detectar decisiones
        triggers = [
            "integration", "authentication", "database",
            "cache", "messaging", "api", "security"
        ]

        story_text = user_story.get("title", "").lower()

        for trigger in triggers:
            if trigger in story_text:
                decisions.append({
                    "title": f"{trigger.capitalize()} approach for {user_story['id']}",
                    "context": user_story["title"],
                    "impact": DecisionImpact.MEDIUM,
                    "requires_spike": True
                })

        return decisions

    def _determine_governance_level(self, decision: Dict) -> GovernanceLevel:
        """Determina nivel de governance requerido"""
        if decision["impact"] == DecisionImpact.CRITICAL:
            return GovernanceLevel.STRATEGIC
        elif decision["impact"] == DecisionImpact.HIGH:
            return GovernanceLevel.TACTICAL
        elif decision["impact"] == DecisionImpact.MEDIUM:
            return GovernanceLevel.TECHNICAL
        else:
            return GovernanceLevel.TEAM

    def _get_domain_from_phase(self, phase: TOGAFPhase) -> str:
        """Mapea fase TOGAF a dominio de arquitectura"""
        mapping = {
            TOGAFPhase.BUSINESS: "Business",
            TOGAFPhase.DATA: "Data",
            TOGAFPhase.APPLICATION: "Application",
            TOGAFPhase.TECHNOLOGY: "Technology"
        }
        return mapping.get(phase, "Application")

    def _identify_stakeholders(self) -> List[str]:
        return ["CTO", "Product Owner", "Lead Architect", "Engineering Managers"]

    def _define_success_metrics(self) -> List[str]:
        return [
            "Time to market < 6 months",
            "System availability > 99.9%",
            "Developer satisfaction > 4/5"
        ]

    def _create_quarterly_roadmap(self) -> Dict:
        return {
            "Q1": "Foundation & Infrastructure",
            "Q2": "Core Services Development",
            "Q3": "Integration & Testing",
            "Q4": "Launch & Optimization"
        }

    def _identify_building_blocks(self, target_state: Dict) -> List[Dict]:
        return []  # Simplified for example

    def _create_migration_path(self, gaps: List[str]) -> List[Dict]:
        return []  # Simplified for example

    def _aligns_with_business_goals(self, adr: ArchitectureDecision) -> bool:
        return True  # Simplified - real implementation would check alignment

    def _follows_architecture_principles(self, adr: ArchitectureDecision) -> bool:
        return True  # Simplified - real implementation would validate principles

    def _calculate_avg_decision_time(self, adrs: List[ArchitectureDecision]) -> float:
        """Calcula tiempo promedio de decisión en días"""
        times = []
        for adr in adrs:
            if adr.decision_date and adr.created_date:
                delta = adr.decision_date - adr.created_date
                times.append(delta.days)

        return sum(times) / len(times) if times else 0

# ==========================================
# EJEMPLO DE USO
# ==========================================

def example_usage():
    """Ejemplo completo de integración ADR + TOGAF + Scrum"""

    framework = IntegratedArchitectureFramework()

    # ========================================
    # QUARTER 1: TOGAF Strategic Planning
    # ========================================

    print("=== Q1: Strategic Planning (TOGAF) ===\n")

    vision = framework.create_architecture_vision(
        business_goals=[
            "Launch e-commerce platform in 6 months",
            "Support 100K concurrent users",
            "Achieve 99.9% uptime"
        ],
        principles=[
            "Cloud-native first",
            "API-first design",
            "Security by default",
            "Microservices for scalability"
        ],
        constraints={
            "budget": "$500K",
            "team_size": "15 engineers",
            "timeline": "6 months"
        }
    )

    print(f"Architecture Vision created: {vision['roadmap_quarters']}\n")

    # Define target architecture
    target_arch = framework.define_target_architecture(
        current_state={"architecture": "Monolith on-premise"},
        target_state={
            "architecture": "Microservices on AWS",
            "services": ["User Service", "Product Service", "Order Service", "Payment Service"]
        },
        gap_analysis=[
            "Need cloud infrastructure",
            "Need API gateway",
            "Need service mesh",
            "Need CI/CD pipeline"
        ]
    )

    print(f"Product Backlog created: {len(target_arch['product_backlog'])} epics\n")

    # ========================================
    # SPRINT 1: Infrastructure Foundation
    # ========================================

    print("=== Sprint 1: Infrastructure Foundation ===\n")

    sprint_1_stories = [
        {
            "id": "US-1",
            "title": "As DevOps, I want to setup Kubernetes cluster",
            "acceptance_criteria": ["EKS cluster running", "kubectl access configured"]
        },
        {
            "id": "US-2",
            "title": "As Developer, I want CI/CD pipeline for deployments",
            "acceptance_criteria": ["GitHub Actions configured", "Auto-deploy to staging"]
        }
    ]

    planning = framework.sprint_planning(
        sprint_number=1,
        user_stories=sprint_1_stories
    )

    print(f"Sprint Planning complete:")
    print(f"  - User Stories: {len(planning['user_stories'])}")
    print(f"  - ADR Drafts created: {len(planning['adr_drafts'])}")
    print(f"  - Spikes planned: {len(planning['spikes'])}\n")

    for adr in planning['adr_drafts']:
        print(f"  ADR-{adr.adr_number}: {adr.title}")

    # ========================================
    # MONTHLY: Architecture Board Review
    # ========================================

    print("\n=== Monthly Architecture Board Review ===\n")

    board_review = framework.architecture_board_review(month=12)

    print(f"Board Review Results:")
    print(f"  - ADRs Reviewed: {board_review['adrs_reviewed']}")
    print(f"  - Approvals: {len(board_review['approvals'])}")
    print(f"  - Concerns: {len(board_review['concerns'])}\n")

if __name__ == "__main__":
    example_usage()
```

---

## 2. Architecture Governance Framework

### Framework de Governance Multi-nivel

```python
from typing import Protocol
from abc import ABC, abstractmethod

# ==========================================
# GOVERNANCE FRAMEWORK
# ==========================================

class GovernancePolicy(Protocol):
    """Protocol para políticas de governance"""
    def evaluate(self, adr: ArchitectureDecision) -> bool: ...
    def get_violations(self, adr: ArchitectureDecision) -> List[str]: ...

class SecurityPolicy:
    """Política de seguridad"""

    def evaluate(self, adr: ArchitectureDecision) -> bool:
        violations = self.get_violations(adr)
        return len(violations) == 0

    def get_violations(self, adr: ArchitectureDecision) -> List[str]:
        violations = []

        # Rule 1: Decisiones de autenticación requieren security review
        if "authentication" in adr.title.lower():
            if "Security Team" not in adr.consulted:
                violations.append("Authentication decisions require Security Team consultation")

        # Rule 2: Decisiones de datos requieren encryption plan
        if "database" in adr.title.lower() or "data" in adr.title.lower():
            if "encryption" not in adr.decision.lower():
                violations.append("Data decisions must address encryption")

        # Rule 3: APIs públicas requieren rate limiting
        if "api" in adr.title.lower() and "public" in adr.context.lower():
            if "rate limit" not in adr.decision.lower():
                violations.append("Public APIs must have rate limiting")

        return violations

class CostPolicy:
    """Política de costos"""

    def __init__(self, max_monthly_cost: float):
        self.max_monthly_cost = max_monthly_cost

    def evaluate(self, adr: ArchitectureDecision) -> bool:
        violations = self.get_violations(adr)
        return len(violations) == 0

    def get_violations(self, adr: ArchitectureDecision) -> List[str]:
        violations = []

        # Extraer costo estimado del ADR
        cost = self._extract_cost_from_adr(adr)

        if cost and cost > self.max_monthly_cost:
            violations.append(
                f"Estimated cost ${cost}/month exceeds limit ${self.max_monthly_cost}"
            )

        # Rule: Decisiones >$10K requieren CFO approval
        if cost and cost > 10000:
            if "CFO" not in adr.consulted:
                violations.append("Decisions >$10K/month require CFO consultation")

        return violations

    def _extract_cost_from_adr(self, adr: ArchitectureDecision) -> Optional[float]:
        """Extrae costo del texto del ADR (simplified)"""
        # En producción, esto sería más sofisticado
        import re
        cost_pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
        matches = re.findall(cost_pattern, adr.decision + adr.context)

        if matches:
            return float(matches[0].replace(',', ''))
        return None

class CompliancePolicy:
    """Política de compliance (PCI-DSS, HIPAA, GDPR, etc.)"""

    def __init__(self, regulations: List[str]):
        self.regulations = regulations

    def evaluate(self, adr: ArchitectureDecision) -> bool:
        violations = self.get_violations(adr)
        return len(violations) == 0

    def get_violations(self, adr: ArchitectureDecision) -> List[str]:
        violations = []

        # PCI-DSS: No almacenar números de tarjeta
        if "PCI-DSS" in self.regulations:
            if "credit card" in adr.context.lower() or "payment" in adr.title.lower():
                if "tokenization" not in adr.decision.lower() and \
                   "third-party" not in adr.decision.lower():
                    violations.append(
                        "PCI-DSS: Must use tokenization or third-party for card data"
                    )

        # GDPR: Derecho al olvido
        if "GDPR" in self.regulations:
            if "user data" in adr.context.lower() or "personal" in adr.context.lower():
                if "deletion" not in adr.decision.lower() and \
                   "right to be forgotten" not in adr.decision.lower():
                    violations.append(
                        "GDPR: Must address data deletion and right to be forgotten"
                    )

        # HIPAA: Audit logs
        if "HIPAA" in self.regulations:
            if "health" in adr.context.lower() or "medical" in adr.context.lower():
                if "audit log" not in adr.decision.lower():
                    violations.append(
                        "HIPAA: Must implement audit logging for health data access"
                    )

        return violations

class ArchitectureGovernanceEngine:
    """
    Motor de governance que aplica políticas a ADRs

    Integra con:
    - TOGAF: Architecture Compliance
    - Scrum: Sprint Planning validation
    - ADRs: Pre-approval checks
    """

    def __init__(self):
        self.policies: List[GovernancePolicy] = []
        self.violations_log: List[Dict] = []

    def register_policy(self, policy: GovernancePolicy):
        """Registra una política de governance"""
        self.policies.append(policy)

    def evaluate_adr(self, adr: ArchitectureDecision) -> Dict:
        """
        Evalúa ADR contra todas las políticas

        Returns:
            {
                "compliant": bool,
                "violations": List[str],
                "recommendations": List[str]
            }
        """
        all_violations = []

        for policy in self.policies:
            violations = policy.get_violations(adr)
            if violations:
                all_violations.extend([
                    f"{policy.__class__.__name__}: {v}" for v in violations
                ])

        result = {
            "adr_number": adr.adr_number,
            "title": adr.title,
            "compliant": len(all_violations) == 0,
            "violations": all_violations,
            "recommendations": self._generate_recommendations(all_violations)
        }

        # Log violations
        if not result["compliant"]:
            self.violations_log.append({
                "date": datetime.now(),
                "adr": adr.adr_number,
                "violations": all_violations
            })

        return result

    def _generate_recommendations(self, violations: List[str]) -> List[str]:
        """Genera recomendaciones basadas en violaciones"""
        recommendations = []

        if any("Security Team" in v for v in violations):
            recommendations.append("Schedule meeting with Security Team")

        if any("cost" in v.lower() for v in violations):
            recommendations.append("Perform detailed cost analysis")

        if any("compliance" in v.lower() or "PCI" in v or "GDPR" in v or "HIPAA" in v):
            recommendations.append("Consult with Legal and Compliance teams")

        return recommendations

    def get_compliance_report(self) -> Dict:
        """Genera reporte de compliance"""
        total_adrs = len(self.violations_log)

        return {
            "total_violations": total_adrs,
            "by_policy": self._violations_by_policy(),
            "trend": self._compliance_trend(),
            "recommendations": self._strategic_recommendations()
        }

    def _violations_by_policy(self) -> Dict[str, int]:
        """Agrupa violaciones por política"""
        by_policy = {}

        for log in self.violations_log:
            for violation in log["violations"]:
                policy = violation.split(":")[0]
                by_policy[policy] = by_policy.get(policy, 0) + 1

        return by_policy

    def _compliance_trend(self) -> str:
        """Analiza tendencia de compliance"""
        # Simplified - real implementation would analyze over time
        return "Improving"

    def _strategic_recommendations(self) -> List[str]:
        """Recomendaciones estratégicas"""
        by_policy = self._violations_by_policy()
        recs = []

        if by_policy.get("SecurityPolicy", 0) > 5:
            recs.append("Consider mandatory security training for architects")

        if by_policy.get("CostPolicy", 0) > 3:
            recs.append("Implement cost estimation template in ADRs")

        if by_policy.get("CompliancePolicy", 0) > 0:
            recs.append("Schedule compliance review with Legal team")

        return recs

# ==========================================
# EJEMPLO: Governance in Action
# ==========================================

def example_governance():
    """Ejemplo de governance en acción"""

    print("=== Architecture Governance Example ===\n")

    # Setup governance engine
    governance = ArchitectureGovernanceEngine()
    governance.register_policy(SecurityPolicy())
    governance.register_policy(CostPolicy(max_monthly_cost=5000))
    governance.register_policy(CompliancePolicy(regulations=["PCI-DSS", "GDPR"]))

    # Create ADR for payment processing
    adr = ArchitectureDecision(
        adr_number=1,
        title="Payment Processing Implementation",
        status="Proposed",
        togaf_phase=TOGAFPhase.APPLICATION,
        architecture_domain="Application",
        business_driver="Enable e-commerce transactions",
        governance_level=GovernanceLevel.TACTICAL,
        impact=DecisionImpact.HIGH,
        requires_board_approval=True,
        sprint_number=5,
        epic="E-commerce Checkout",
        user_stories=["US-101: Process credit card payments"],
        context="""
        Need to implement credit card payment processing for e-commerce platform.
        Expected volume: 10K transactions/month.
        Must be PCI-DSS compliant.
        """,
        options_considered=[],
        decision="""
        We will use Stripe API for payment processing.
        Estimated cost: $3,000/month in transaction fees.
        Stripe handles PCI-DSS compliance through tokenization.
        """,
        consequences={
            "positive": ["No PCI compliance overhead", "Fast time to market"],
            "negative": ["Vendor lock-in", "Transaction fees"],
            "risks": ["Stripe API availability"]
        },
        deciders=["Tech Lead", "Product Owner"],
        consulted=["Security Team"],  # Good - security consulted
        informed=["Development Team"],
        created_date=datetime.now(),
        decision_date=None,
        review_date=None,
        superseded_by=None
    )

    # Evaluate ADR
    evaluation = governance.evaluate_adr(adr)

    print(f"ADR-{evaluation['adr_number']}: {evaluation['title']}")
    print(f"Compliant: {evaluation['compliant']}")

    if evaluation['violations']:
        print(f"\nViolations:")
        for violation in evaluation['violations']:
            print(f"  ❌ {violation}")
    else:
        print("  ✅ No violations found")

    if evaluation['recommendations']:
        print(f"\nRecommendations:")
        for rec in evaluation['recommendations']:
            print(f"  💡 {rec}")

    print("\n" + "="*50 + "\n")

    # Create non-compliant ADR
    bad_adr = ArchitectureDecision(
        adr_number=2,
        title="User Authentication System",
        status="Proposed",
        togaf_phase=TOGAFPhase.APPLICATION,
        architecture_domain="Application",
        business_driver="Secure user access",
        governance_level=GovernanceLevel.TACTICAL,
        impact=DecisionImpact.HIGH,
        requires_board_approval=True,
        sprint_number=3,
        epic="User Management",
        user_stories=["US-50: User login"],
        context="Need authentication for user accounts with personal data (GDPR applicable)",
        options_considered=[],
        decision="We will implement custom JWT authentication with bcrypt password hashing",
        consequences={"positive": [], "negative": [], "risks": []},
        deciders=["Developer"],
        consulted=[],  # ❌ Missing Security Team
        informed=[],
        created_date=datetime.now(),
        decision_date=None,
        review_date=None,
        superseded_by=None
    )

    evaluation2 = governance.evaluate_adr(bad_adr)

    print(f"ADR-{evaluation2['adr_number']}: {evaluation2['title']}")
    print(f"Compliant: {evaluation2['compliant']}")

    if evaluation2['violations']:
        print(f"\nViolations:")
        for violation in evaluation2['violations']:
            print(f"  ❌ {violation}")

    if evaluation2['recommendations']:
        print(f"\nRecommendations:")
        for rec in evaluation2['recommendations']:
            print(f"  💡 {rec}")

if __name__ == "__main__":
    example_governance()
```

---

## 3. Sprint Workflow con ADRs

### Workflow Completo Sprint-by-Sprint

```python
from enum import Enum
from typing import Callable
import asyncio

# ==========================================
# SPRINT WORKFLOW INTEGRADO
# ==========================================

class SprintPhase(Enum):
    """Fases del sprint"""
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    RETROSPECTIVE = "retrospective"

class SprintWorkflow:
    """
    Workflow completo de sprint con integración ADR

    Estructura:
    - Day 1: Sprint Planning + ADR Identification
    - Days 2-9: Execution + ADR Decision Making
    - Day 10: Review + Retro + ADR Presentation
    """

    def __init__(self, framework: IntegratedArchitectureFramework):
        self.framework = framework
        self.current_phase = SprintPhase.PLANNING
        self.sprint_log: List[Dict] = []

    # ========================================
    # DAY 1: SPRINT PLANNING
    # ========================================

    def day_1_sprint_planning(
        self,
        sprint_number: int,
        sprint_goal: str,
        user_stories: List[Dict],
        team: List[str]
    ) -> Dict:
        """
        Day 1: Sprint Planning Meeting

        Agenda:
        1. Product Owner presents sprint goal
        2. Team reviews user stories
        3. Identify architecture decisions needed
        4. Create ADR drafts
        5. Estimate stories + spikes
        6. Commit to sprint backlog

        Duration: 4 hours
        """
        print(f"\n{'='*60}")
        print(f"SPRINT {sprint_number} PLANNING - Day 1")
        print(f"{'='*60}\n")

        print(f"Sprint Goal: {sprint_goal}\n")

        planning_result = {
            "sprint_number": sprint_number,
            "sprint_goal": sprint_goal,
            "team": team,
            "committed_stories": [],
            "adr_drafts": [],
            "spikes": [],
            "capacity": len(team) * 10,  # 10 story points per person
            "estimated_points": 0
        }

        # Step 1: Review each user story
        print("📋 Reviewing User Stories:\n")
        for story in user_stories:
            print(f"  {story['id']}: {story['title']}")
            print(f"    Estimate: {story.get('points', '?')} points")

            # Step 2: Identify architecture decisions
            decisions = self._identify_decisions_in_story(story)

            if decisions:
                print(f"    🏗️  Architecture Decisions Needed:")
                for decision in decisions:
                    print(f"      - {decision['title']}")

                    # Create ADR draft
                    adr = self.framework._create_adr(
                        title=decision['title'],
                        togaf_phase=TOGAFPhase.APPLICATION,
                        governance_level=decision['governance_level'],
                        impact=decision['impact'],
                        context=decision['context'],
                        sprint_number=sprint_number,
                        user_stories=[story['id']]
                    )

                    adr.deciders = team
                    planning_result['adr_drafts'].append(adr)

                    # Create spike if needed
                    if decision.get('requires_spike'):
                        spike = {
                            "title": f"Spike: {decision['title']}",
                            "adr": adr.adr_number,
                            "timeboxed": "4 hours",
                            "assignee": team[0],  # Assign to first team member
                            "outcome": "Update ADR with research findings"
                        }
                        planning_result['spikes'].append(spike)
                        print(f"        📊 Spike created: {spike['timeboxed']} timebox")

            # Add to committed stories if fits capacity
            story_points = story.get('points', 0)
            if planning_result['estimated_points'] + story_points <= planning_result['capacity']:
                planning_result['committed_stories'].append(story)
                planning_result['estimated_points'] += story_points
                print(f"    ✅ Committed to sprint")
            else:
                print(f"    ⚠️  Deferred - exceeds capacity")

            print()

        # Summary
        print(f"📊 Planning Summary:")
        print(f"  Committed Stories: {len(planning_result['committed_stories'])}")
        print(f"  Total Points: {planning_result['estimated_points']}/{planning_result['capacity']}")
        print(f"  ADR Drafts Created: {len(planning_result['adr_drafts'])}")
        print(f"  Spikes Planned: {len(planning_result['spikes'])}")

        # Log
        self.sprint_log.append({
            "day": 1,
            "phase": "planning",
            "result": planning_result
        })

        return planning_result

    # ========================================
    # DAYS 2-3: SPIKE EXECUTION
    # ========================================

    def day_2_3_spike_research(
        self,
        spike: Dict,
        research_findings: Dict
    ) -> Dict:
        """
        Days 2-3: Execute spikes para research de decisiones

        Process:
        1. Developer investiga opciones
        2. Documenta hallazgos
        3. Actualiza ADR draft con opciones consideradas
        4. Prepara presentación para equipo

        Duration: 4 hours (timeboxed)
        """
        print(f"\n{'='*60}")
        print(f"SPIKE RESEARCH - Days 2-3")
        print(f"{'='*60}\n")

        print(f"🔬 Spike: {spike['title']}")
        print(f"⏱️  Timebox: {spike['timeboxed']}")
        print(f"👤 Assignee: {spike['assignee']}\n")

        # Update ADR with research findings
        adr = self.framework.adrs[spike['adr']]

        print(f"📝 Research Findings:\n")

        # Document options considered
        for option in research_findings['options']:
            print(f"  Option: {option['name']}")
            print(f"    Pros: {', '.join(option['pros'])}")
            print(f"    Cons: {', '.join(option['cons'])}")
            print(f"    Cost: {option.get('cost', 'TBD')}")
            print(f"    Complexity: {option.get('complexity', 'TBD')}")
            print()

            adr.options_considered.append(option)

        # Add recommendation
        if research_findings.get('recommendation'):
            print(f"💡 Recommendation: {research_findings['recommendation']['option']}")
            print(f"   Reason: {research_findings['recommendation']['reason']}\n")

        # Update ADR status
        adr.status = "Proposed"

        spike_result = {
            "spike": spike['title'],
            "adr": adr.adr_number,
            "options_evaluated": len(research_findings['options']),
            "recommendation": research_findings.get('recommendation'),
            "ready_for_decision": True
        }

        self.sprint_log.append({
            "day": 2,
            "phase": "spike_research",
            "result": spike_result
        })

        return spike_result

    # ========================================
    # DAY 4: TEAM DECISION MEETING
    # ========================================

    def day_4_team_decision_meeting(
        self,
        adr_number: int,
        team_discussion: Dict
    ) -> Dict:
        """
        Day 4: Team Decision Meeting

        Agenda:
        1. Review spike findings
        2. Team discussion on options
        3. Consider trade-offs
        4. Make decision
        5. Document rationale
        6. Update ADR

        Duration: 1 hour
        """
        print(f"\n{'='*60}")
        print(f"TEAM DECISION MEETING - Day 4")
        print(f"{'='*60}\n")

        adr = self.framework.adrs[adr_number]

        print(f"📄 ADR-{adr.adr_number}: {adr.title}\n")

        print(f"👥 Team Discussion:\n")
        for comment in team_discussion.get('comments', []):
            print(f"  {comment['person']}: {comment['comment']}")

        print(f"\n🎯 Decision: {team_discussion['decision']}\n")
        print(f"📖 Rationale: {team_discussion['rationale']}\n")

        # Update ADR
        adr.decision = team_discussion['decision']
        adr.status = "Accepted"
        adr.decision_date = datetime.now()
        adr.consequences = team_discussion.get('consequences', {
            "positive": [],
            "negative": [],
            "risks": []
        })

        # Check if needs Architecture Board approval
        if adr.requires_board_approval:
            print(f"⚠️  This decision requires Architecture Board approval")
            print(f"   Will be presented in next monthly review\n")
            adr.status = "Pending Board Approval"
        else:
            print(f"✅ Decision approved - team has authority\n")

        decision_result = {
            "adr": adr.adr_number,
            "decision": team_discussion['decision'],
            "status": adr.status,
            "requires_escalation": adr.requires_board_approval
        }

        self.sprint_log.append({
            "day": 4,
            "phase": "decision_meeting",
            "result": decision_result
        })

        return decision_result

    # ========================================
    # DAYS 5-9: IMPLEMENTATION
    # ========================================

    def day_5_9_implementation(
        self,
        user_story: Dict,
        adr_numbers: List[int],
        daily_updates: List[Dict]
    ) -> Dict:
        """
        Days 5-9: Implementation siguiendo las decisiones

        Process:
        1. Implement según ADRs aceptados
        2. Daily standup: report ADR implementation progress
        3. Update ADR con implementation notes
        4. Flag any issues that require ADR revision

        Duration: 5 days
        """
        print(f"\n{'='*60}")
        print(f"IMPLEMENTATION - Days 5-9")
        print(f"{'='*60}\n")

        print(f"🚀 Implementing: {user_story['title']}\n")

        print(f"📋 Following ADRs:")
        for adr_num in adr_numbers:
            adr = self.framework.adrs[adr_num]
            print(f"  ADR-{adr.adr_number}: {adr.title} - {adr.status}")

        print(f"\n📅 Daily Updates:\n")

        implementation_issues = []

        for update in daily_updates:
            print(f"Day {update['day']}:")
            print(f"  Progress: {update['progress']}")

            if update.get('adr_issues'):
                print(f"  ⚠️  ADR Issues:")
                for issue in update['adr_issues']:
                    print(f"    - {issue}")
                    implementation_issues.append(issue)

            if update.get('adr_learnings'):
                print(f"  💡 Learnings:")
                for learning in update['adr_learnings']:
                    print(f"    - {learning}")

            print()

        # If issues found, flag for retro
        impl_result = {
            "user_story": user_story['id'],
            "adrs_followed": adr_numbers,
            "implementation_issues": implementation_issues,
            "status": "completed" if not implementation_issues else "completed_with_issues"
        }

        self.sprint_log.append({
            "day": 5-9,
            "phase": "implementation",
            "result": impl_result
        })

        return impl_result

    # ========================================
    # DAY 10: SPRINT REVIEW + RETRO
    # ========================================

    def day_10_sprint_review(
        self,
        sprint_number: int,
        stakeholders: List[str]
    ) -> Dict:
        """
        Day 10 Part 1: Sprint Review

        Agenda:
        1. Demo working software
        2. Present architecture decisions made (ADRs)
        3. Stakeholder feedback
        4. Identify decisions for Architecture Board

        Duration: 2 hours
        """
        print(f"\n{'='*60}")
        print(f"SPRINT {sprint_number} REVIEW - Day 10")
        print(f"{'='*60}\n")

        print(f"👥 Stakeholders: {', '.join(stakeholders)}\n")

        # Part 1: Demo
        print(f"🎬 Demo: Working Software\n")
        print(f"  [Demo of implemented features]\n")

        # Part 2: ADRs Presentation
        print(f"📄 Architecture Decisions Made This Sprint:\n")

        sprint_adrs = [
            adr for adr in self.framework.adrs.values()
            if adr.sprint_number == sprint_number
        ]

        review_result = {
            "sprint": sprint_number,
            "adrs_presented": [],
            "stakeholder_feedback": [],
            "escalations": []
        }

        for adr in sprint_adrs:
            print(f"  ADR-{adr.adr_number}: {adr.title}")
            print(f"    Status: {adr.status}")
            print(f"    Decision: {adr.decision[:100]}...")
            print(f"    Impact: {adr.impact.value}")

            adr_summary = {
                "number": adr.adr_number,
                "title": adr.title,
                "decision": adr.decision,
                "status": adr.status
            }
            review_result['adrs_presented'].append(adr_summary)

            # Check if needs escalation
            if adr.requires_board_approval:
                print(f"    ⚠️  Requires Architecture Board approval")
                review_result['escalations'].append(adr.adr_number)

            print()

        # Stakeholder feedback
        print(f"💬 Stakeholder Feedback:")
        print(f"  [Collect feedback on decisions and implementation]\n")

        self.sprint_log.append({
            "day": 10,
            "phase": "review",
            "result": review_result
        })

        return review_result

    def day_10_sprint_retrospective(self, sprint_number: int) -> Dict:
        """
        Day 10 Part 2: Sprint Retrospective

        Focus on ADR process:
        1. Was decision-making effective?
        2. Did we involve right people?
        3. Were ADRs helpful or bureaucratic?
        4. Process improvements

        Duration: 1.5 hours
        """
        print(f"\n{'='*60}")
        print(f"SPRINT {sprint_number} RETROSPECTIVE - Day 10")
        print(f"{'='*60}\n")

        # Analyze ADR metrics for this sprint
        sprint_adrs = [
            adr for adr in self.framework.adrs.values()
            if adr.sprint_number == sprint_number
        ]

        retro_result = {
            "sprint": sprint_number,
            "what_went_well": [],
            "what_to_improve": [],
            "action_items": []
        }

        # Metric 1: Decision time
        avg_decision_time = self._calculate_avg_decision_time(sprint_adrs)

        print(f"📊 ADR Metrics:\n")
        print(f"  ADRs created: {len(sprint_adrs)}")
        print(f"  Avg decision time: {avg_decision_time:.1f} days")

        if avg_decision_time < 3:
            retro_result['what_went_well'].append(
                f"Fast decision making: {avg_decision_time:.1f} days average"
            )
            print(f"  ✅ Fast decision making\n")
        else:
            retro_result['what_to_improve'].append(
                f"Slow decisions: {avg_decision_time:.1f} days - target is <3 days"
            )
            retro_result['action_items'].append(
                "Action: Schedule dedicated decision meetings earlier in sprint"
            )
            print(f"  ⚠️  Decisions taking too long\n")

        # Metric 2: Team involvement
        print(f"👥 Team Involvement:\n")
        for adr in sprint_adrs:
            consulted_count = len(adr.consulted)
            print(f"  ADR-{adr.adr_number}: {consulted_count} people consulted")

            if consulted_count == 0 and adr.impact in [DecisionImpact.HIGH, DecisionImpact.CRITICAL]:
                retro_result['what_to_improve'].append(
                    f"ADR-{adr.adr_number}: High-impact decision with no stakeholder consultation"
                )

        print()

        # Team discussion
        print(f"💭 Team Discussion:\n")
        print(f"What went well:")
        for item in retro_result['what_went_well']:
            print(f"  ✅ {item}")

        print(f"\nWhat to improve:")
        for item in retro_result['what_to_improve']:
            print(f"  🔧 {item}")

        print(f"\nAction items:")
        for item in retro_result['action_items']:
            print(f"  🎯 {item}")

        print()

        self.sprint_log.append({
            "day": 10,
            "phase": "retrospective",
            "result": retro_result
        })

        return retro_result

    # ========================================
    # HELPER METHODS
    # ========================================

    def _identify_decisions_in_story(self, story: Dict) -> List[Dict]:
        """Identifica decisiones arquitectónicas en user story"""
        decisions = []

        # Keywords que indican decisión arquitectónica
        decision_keywords = {
            "authentication": {
                "title": "Authentication Strategy",
                "governance_level": GovernanceLevel.TACTICAL,
                "impact": DecisionImpact.HIGH,
                "requires_spike": True
            },
            "database": {
                "title": "Database Selection",
                "governance_level": GovernanceLevel.TACTICAL,
                "impact": DecisionImpact.HIGH,
                "requires_spike": True
            },
            "api": {
                "title": "API Design Approach",
                "governance_level": GovernanceLevel.TECHNICAL,
                "impact": DecisionImpact.MEDIUM,
                "requires_spike": False
            },
            "cache": {
                "title": "Caching Strategy",
                "governance_level": GovernanceLevel.TECHNICAL,
                "impact": DecisionImpact.MEDIUM,
                "requires_spike": True
            },
            "messaging": {
                "title": "Message Queue Selection",
                "governance_level": GovernanceLevel.TACTICAL,
                "impact": DecisionImpact.HIGH,
                "requires_spike": True
            },
            "payment": {
                "title": "Payment Processing Approach",
                "governance_level": GovernanceLevel.STRATEGIC,
                "impact": DecisionImpact.CRITICAL,
                "requires_spike": True
            }
        }

        story_text = story.get('title', '').lower() + ' ' + story.get('description', '').lower()

        for keyword, template in decision_keywords.items():
            if keyword in story_text:
                decision = template.copy()
                decision['context'] = f"Needed for {story['id']}: {story['title']}"
                decisions.append(decision)

        return decisions

    def _calculate_avg_decision_time(self, adrs: List[ArchitectureDecision]) -> float:
        """Calcula tiempo promedio de decisión"""
        times = []
        for adr in adrs:
            if adr.decision_date and adr.created_date:
                delta = adr.decision_date - adr.created_date
                times.append(delta.days + delta.seconds / 86400)  # Include partial days

        return sum(times) / len(times) if times else 0.0

# ==========================================
# EJEMPLO COMPLETO: Full Sprint
# ==========================================

def example_full_sprint():
    """Ejemplo de sprint completo con ADRs"""

    # Setup
    framework = IntegratedArchitectureFramework()
    workflow = SprintWorkflow(framework)

    # ========================================
    # DAY 1: SPRINT PLANNING
    # ========================================

    user_stories = [
        {
            "id": "US-101",
            "title": "As a user, I want to login with email and password",
            "description": "Implement authentication system",
            "points": 5,
            "acceptance_criteria": [
                "User can register with email/password",
                "User can login",
                "JWT tokens issued"
            ]
        },
        {
            "id": "US-102",
            "title": "As a user, I want to view my profile",
            "description": "Display user profile with data from database",
            "points": 3,
            "acceptance_criteria": [
                "Fetch user data from database",
                "Display in UI"
            ]
        },
        {
            "id": "US-103",
            "title": "As a user, I want to receive email notifications",
            "description": "Send email when important events occur",
            "points": 5,
            "acceptance_criteria": [
                "Queue email jobs",
                "Process async",
                "Handle failures"
            ]
        }
    ]

    planning = workflow.day_1_sprint_planning(
        sprint_number=5,
        sprint_goal="Implement user authentication and profile",
        user_stories=user_stories,
        team=["Alice", "Bob", "Charlie", "Diana"]
    )

    # ========================================
    # DAYS 2-3: SPIKE RESEARCH
    # ========================================

    # Spike for authentication decision
    auth_spike = planning['spikes'][0]

    research_findings = {
        "options": [
            {
                "name": "JWT with bcrypt",
                "pros": ["Simple", "Stateless", "Widely used"],
                "cons": ["Token revocation complex", "Need to implement carefully"],
                "cost": "$0",
                "complexity": "Medium"
            },
            {
                "name": "Auth0",
                "pros": ["Managed service", "Many features", "Secure by default"],
                "cons": ["Cost", "Vendor lock-in"],
                "cost": "$200/month",
                "complexity": "Low"
            },
            {
                "name": "OAuth2 + Keycloak",
                "pros": ["Open source", "Standards-based", "Enterprise features"],
                "cons": ["Complex setup", "Ops overhead"],
                "cost": "$50/month (hosting)",
                "complexity": "High"
            }
        ],
        "recommendation": {
            "option": "JWT with bcrypt",
            "reason": "Best balance of simplicity, cost, and control for our scale"
        }
    }

    spike_result = workflow.day_2_3_spike_research(auth_spike, research_findings)

    # ========================================
    # DAY 4: TEAM DECISION
    # ========================================

    team_discussion = {
        "comments": [
            {"person": "Alice", "comment": "JWT is good, but we need refresh tokens"},
            {"person": "Bob", "comment": "Agreed, and rate limiting on login endpoint"},
            {"person": "Charlie", "comment": "Let's use Redis for token blacklist"},
            {"person": "Diana", "comment": "We should also add 2FA in next sprint"}
        ],
        "decision": """
        Implement JWT authentication with bcrypt password hashing.
        - Access tokens: 15 min expiry
        - Refresh tokens: 7 day expiry, stored in Redis
        - Token blacklist in Redis for logout
        - Rate limiting: 5 attempts per 15 min per IP
        """,
        "rationale": """
        JWT provides stateless authentication which scales better than sessions.
        Refresh tokens balance security (short-lived access tokens) with UX.
        Redis blacklist solves token revocation problem.
        Cost effective ($0 vs $200/month for Auth0).
        Team has expertise with JWT.
        """,
        "consequences": {
            "positive": [
                "Stateless - scales horizontally",
                "No vendor lock-in",
                "Full control over auth logic",
                "Zero external cost"
            ],
            "negative": [
                "We own security implementation",
                "Need to implement refresh token rotation",
                "Redis dependency"
            ],
            "risks": [
                "JWT security vulnerabilities if implemented incorrectly",
                "Redis becomes single point of failure (mitigate with Redis Cluster)"
            ]
        }
    }

    decision_result = workflow.day_4_team_decision_meeting(
        adr_number=spike_result['adr'],
        team_discussion=team_discussion
    )

    # ========================================
    # DAYS 5-9: IMPLEMENTATION
    # ========================================

    daily_updates = [
        {
            "day": 5,
            "progress": "Setup JWT library, implement token generation",
            "adr_issues": [],
            "adr_learnings": ["JWT library makes this easy"]
        },
        {
            "day": 6,
            "progress": "Implement bcrypt password hashing, user registration",
            "adr_issues": [],
            "adr_learnings": ["Bcrypt work factor of 12 provides good security/performance balance"]
        },
        {
            "day": 7,
            "progress": "Implement refresh tokens with Redis",
            "adr_issues": ["Redis connection pooling needed - not in ADR"],
            "adr_learnings": ["Should have included Redis connection strategy in ADR"]
        },
        {
            "day": 8,
            "progress": "Implement rate limiting, token blacklist",
            "adr_issues": [],
            "adr_learnings": ["Rate limiting prevents brute force attacks effectively"]
        },
        {
            "day": 9,
            "progress": "Testing, bug fixes, documentation",
            "adr_issues": [],
            "adr_learnings": ["Implementation matched ADR well overall"]
        }
    ]

    impl_result = workflow.day_5_9_implementation(
        user_story=user_stories[0],
        adr_numbers=[spike_result['adr']],
        daily_updates=daily_updates
    )

    # ========================================
    # DAY 10: REVIEW + RETRO
    # ========================================

    review = workflow.day_10_sprint_review(
        sprint_number=5,
        stakeholders=["Product Owner", "CTO", "Security Lead"]
    )

    retro = workflow.day_10_sprint_retrospective(sprint_number=5)

    print(f"\n{'='*60}")
    print(f"SPRINT 5 COMPLETE")
    print(f"{'='*60}\n")

    print(f"📊 Sprint Summary:")
    print(f"  Stories Completed: {len(planning['committed_stories'])}")
    print(f"  ADRs Created: {len(planning['adr_drafts'])}")
    print(f"  Architecture Board Escalations: {len(review['escalations'])}")
    print(f"  Retro Action Items: {len(retro['action_items'])}")

if __name__ == "__main__":
    example_full_sprint()
```

---

## 4. TOGAF ADM Adaptado a Agile

### TOGAF ADM Ligero para Sprints

```python
# ==========================================
# TOGAF ADM AGILE ADAPTATION
# ==========================================

class AgileTO GAFPhaseExecutor:
    """
    TOGAF ADM adaptado para entrega Agile

    Cambios clave:
    - Phases → Sprints (2 weeks vs 3 months)
    - Heavy docs → Lightweight artifacts
    - Waterfall → Iterative
    - Governance → Continuous review
    """

    def __init__(self):
        self.architecture_repository: Dict = {}
        self.current_phase: TOGAFPhase = TOGAFPhase.PRELIMINARY

    # ========================================
    # PRELIMINARY: Architecture Foundation
    # ========================================

    def preliminary_phase_agile(self) -> Dict:
        """
        Preliminary Phase - Adaptación Agile

        TOGAF Traditional:
        - Duration: 1-2 months
        - Output: 50+ page framework document
        - Heavy governance setup

        Agile Adaptation:
        - Duration: 2 days
        - Output: 2-page architecture charter
        - Lightweight governance
        """
        charter = {
            "architecture_vision": "Cloud-native microservices platform",
            "scope": "E-commerce platform for 100K users",
            "principles": [
                "API-first design",
                "Security by default",
                "Autonomous teams",
                "Automated everything"
            ],
            "governance_model": {
                "architecture_board": ["CTO", "Lead Architects"],
                "review_frequency": "Monthly",
                "approval_required_for": [
                    "New technology stack",
                    "Architectural patterns",
                    "Costs >$10K/month"
                ]
            },
            "stakeholders": {
                "business": ["CEO", "Product Owner"],
                "technical": ["CTO", "Engineering Managers"],
                "operations": ["DevOps Lead"]
            }
        }

        self.architecture_repository['charter'] = charter
        return charter

    # ========================================
    # PHASE A: Architecture Vision (Sprint 0)
    # ========================================

    def phase_a_vision_agile(self, sprint_duration_weeks: int = 2) -> Dict:
        """
        Phase A: Architecture Vision - Adaptación Agile

        TOGAF Traditional:
        - Duration: 4-6 weeks
        - Output: Architecture Vision Document (30+ pages)
        - Detailed business scenarios

        Agile Adaptation:
        - Duration: 1 sprint (2 weeks)
        - Output: Vision statement + roadmap (5 pages)
        - High-level epics
        """
        vision = {
            "business_drivers": [
                "Enter e-commerce market in 6 months",
                "Support 100K concurrent users",
                "24/7 availability required",
                "Global customer base (multi-region)"
            ],
            "architecture_vision_statement": """
            Cloud-native microservices platform on AWS enabling rapid
            feature delivery through autonomous teams, supporting 100K
            concurrent users with 99.9% uptime.
            """,
            "target_architecture_summary": {
                "style": "Microservices",
                "cloud": "AWS (multi-region)",
                "data": "Database per service + Event sourcing",
                "integration": "REST APIs + Event-driven",
                "deployment": "Kubernetes (EKS)"
            },
            "roadmap_quarters": {
                "Q1": "Infrastructure + Core Services",
                "Q2": "Business Logic + Integrations",
                "Q3": "Optimization + Advanced Features",
                "Q4": "Launch + Scale"
            },
            "success_metrics": [
                "Deploy to production in < 6 months",
                "99.9% uptime",
                "< 200ms API response time (p95)",
                "Deploy 10+ times per day"
            ]
        }

        # Convert to Product Backlog Epics
        epics = self._vision_to_epics(vision)

        self.architecture_repository['vision'] = vision
        self.architecture_repository['epics'] = epics

        return {
            "vision": vision,
            "epics": epics,
            "duration": f"{sprint_duration_weeks} weeks",
            "output_pages": "~5 pages (vs 30+ in traditional TOGAF)"
        }

    def _vision_to_epics(self, vision: Dict) -> List[Dict]:
        """Convierte vision a epics para product backlog"""
        epics = []

        # Epic 1: Infrastructure
        epics.append({
            "id": "EPIC-1",
            "title": "Cloud Infrastructure Foundation",
            "business_value": vision['business_drivers'][0],
            "architecture_component": vision['target_architecture_summary']['cloud'],
            "estimated_sprints": 2
        })

        # Epic 2: Core Services
        epics.append({
            "id": "EPIC-2",
            "title": "Core Microservices (User, Product, Order)",
            "business_value": vision['business_drivers'][1],
            "architecture_component": vision['target_architecture_summary']['style'],
            "estimated_sprints": 4
        })

        # Epic 3: Data Layer
        epics.append({
            "id": "EPIC-3",
            "title": "Data Layer (Databases + Events)",
            "business_value": vision['business_drivers'][2],
            "architecture_component": vision['target_architecture_summary']['data'],
            "estimated_sprints": 3
        })

        return epics

    # ========================================
    # PHASE B-D: Target Architecture (Sprints 1-2)
    # ========================================

    def phase_b_d_target_architecture_agile(self) -> Dict:
        """
        Phases B-D: Business, Data, Application, Technology Architecture

        TOGAF Traditional:
        - Duration: 3-4 months (each phase separately)
        - Output: 100+ pages of architecture documents
        - Detailed models (UML, ERDs, etc.)

        Agile Adaptation:
        - Duration: 2 sprints (4 weeks total)
        - Output: Architecture Building Blocks (20 pages)
        - Lightweight diagrams (C4, simple ERDs)
        """

        # Business Architecture (simplified)
        business_arch = {
            "business_capabilities": [
                "Customer Management",
                "Product Catalog",
                "Order Processing",
                "Payment Processing",
                "Inventory Management"
            ],
            "value_streams": [
                "Customer Acquisition",
                "Order Fulfillment",
                "Customer Support"
            ]
        }

        # Data Architecture (simplified)
        data_arch = {
            "data_domains": [
                "Customer Data",
                "Product Data",
                "Order Data",
                "Payment Data"
            ],
            "data_strategy": "Database per service + Event sourcing for audit",
            "master_data": "Customer (User Service owns)",
            "data_quality": "Validation at API boundary"
        }

        # Application Architecture (simplified)
        app_arch = {
            "services": [
                {
                    "name": "User Service",
                    "responsibility": "User registration, authentication, profile",
                    "database": "PostgreSQL",
                    "apis": ["POST /users", "POST /auth/login", "GET /users/{id}"]
                },
                {
                    "name": "Product Service",
                    "responsibility": "Product catalog, search, inventory",
                    "database": "PostgreSQL + Elasticsearch",
                    "apis": ["GET /products", "GET /products/{id}", "POST /products/search"]
                },
                {
                    "name": "Order Service",
                    "responsibility": "Order creation, tracking, fulfillment",
                    "database": "PostgreSQL + Event Store",
                    "apis": ["POST /orders", "GET /orders/{id}", "PUT /orders/{id}/status"]
                }
            ],
            "patterns": [
                "API Gateway (Kong)",
                "Service Mesh (Istio)",
                "Event-Driven (Kafka)"
            ]
        }

        # Technology Architecture (simplified)
        tech_arch = {
            "platform": "AWS EKS (Kubernetes)",
            "compute": "Docker containers",
            "databases": ["PostgreSQL (RDS)", "Redis (ElastiCache)", "Elasticsearch"],
            "messaging": "Apache Kafka (MSK)",
            "observability": "Prometheus + Grafana + Jaeger",
            "cicd": "GitHub Actions + ArgoCD"
        }

        # Generate Architecture Building Blocks (ABBs)
        abbs = self._create_architecture_building_blocks(
            business_arch,
            data_arch,
            app_arch,
            tech_arch
        )

        # Gap Analysis
        gaps = self._perform_gap_analysis(
            current_state={"architecture": "Monolith"},
            target_state={"architecture": "Microservices"}
        )

        target_arch = {
            "business": business_arch,
            "data": data_arch,
            "application": app_arch,
            "technology": tech_arch,
            "building_blocks": abbs,
            "gaps": gaps,
            "migration_approach": "Strangler Fig Pattern"
        }

        self.architecture_repository['target_architecture'] = target_arch

        return target_arch

    def _create_architecture_building_blocks(
        self,
        business_arch: Dict,
        data_arch: Dict,
        app_arch: Dict,
        tech_arch: Dict
    ) -> List[Dict]:
        """Crea Architecture Building Blocks desde las arquitecturas"""

        abbs = []

        # ABB para cada microservicio
        for service in app_arch['services']:
            abb = {
                "type": "Application Building Block",
                "name": service['name'],
                "business_capability": service['responsibility'],
                "technology": {
                    "runtime": "Python FastAPI + Docker",
                    "database": service['database'],
                    "deployment": "Kubernetes Deployment"
                },
                "interfaces": service['apis'],
                "dependencies": ["API Gateway", "Service Mesh"],
                "nfrs": {
                    "availability": "99.9%",
                    "response_time": "<200ms p95",
                    "scalability": "Auto-scale 2-20 pods"
                }
            }
            abbs.append(abb)

        # ABB para shared components
        abbs.append({
            "type": "Technology Building Block",
            "name": "API Gateway",
            "technology": "Kong",
            "responsibilities": ["Routing", "Authentication", "Rate Limiting"],
            "nfrs": {"availability": "99.99%"}
        })

        return abbs

    def _perform_gap_analysis(
        self,
        current_state: Dict,
        target_state: Dict
    ) -> List[Dict]:
        """Análisis de gaps entre estado actual y objetivo"""

        return [
            {
                "gap": "No cloud infrastructure",
                "impact": "Cannot deploy microservices",
                "solution": "Setup AWS EKS cluster",
                "priority": "Critical",
                "estimated_effort": "2 sprints"
            },
            {
                "gap": "Monolithic database",
                "impact": "Cannot scale services independently",
                "solution": "Decompose into service databases",
                "priority": "High",
                "estimated_effort": "4 sprints"
            },
            {
                "gap": "No event-driven architecture",
                "impact": "Tight coupling between services",
                "solution": "Implement Kafka for async communication",
                "priority": "Medium",
                "estimated_effort": "2 sprints"
            }
        ]

    # ========================================
    # PHASE E-F: Opportunities & Migration (Continuous)
    # ========================================

    def phase_e_f_migration_planning_agile(
        self,
        target_architecture: Dict
    ) -> Dict:
        """
        Phases E-F: Migration Planning

        TOGAF Traditional:
        - Duration: 2 months
        - Output: Detailed migration plan (40+ pages)
        - Gantt charts, resource allocation

        Agile Adaptation:
        - Duration: 1 week
        - Output: Prioritized backlog with migration stories
        - Continuous planning (adjust each sprint)
        """

        # Prioritize gaps by business value & risk
        prioritized_gaps = sorted(
            target_architecture['gaps'],
            key=lambda x: {"Critical": 0, "High": 1, "Medium": 2}.get(x['priority'], 3)
        )

        # Create migration user stories
        migration_stories = []

        for gap in prioritized_gaps:
            story = {
                "id": f"MIG-{len(migration_stories) + 1}",
                "title": gap['solution'],
                "gap_addressed": gap['gap'],
                "business_value": gap['impact'],
                "estimated_sprints": gap['estimated_effort'],
                "priority": gap['priority'],
                "acceptance_criteria": [
                    "Gap analysis completed",
                    "Solution implemented",
                    "Tests passed",
                    "Documented"
                ]
            }
            migration_stories.append(story)

        # Create migration roadmap
        roadmap = {
            "approach": "Strangler Fig Pattern",
            "phases": [
                {
                    "name": "Phase 1: Foundation",
                    "sprints": "1-4",
                    "goal": "Setup infrastructure",
                    "stories": [s for s in migration_stories if s['priority'] == "Critical"]
                },
                {
                    "name": "Phase 2: Core Services",
                    "sprints": "5-10",
                    "goal": "Extract core microservices",
                    "stories": [s for s in migration_stories if s['priority'] == "High"]
                },
                {
                    "name": "Phase 3: Optimization",
                    "sprints": "11-15",
                    "goal": "Events, caching, monitoring",
                    "stories": [s for s in migration_stories if s['priority'] == "Medium"]
                }
            ],
            "risks": [
                {
                    "risk": "Data migration failures",
                    "mitigation": "Dual-write pattern during transition",
                    "owner": "Data Team"
                },
                {
                    "risk": "Performance degradation",
                    "mitigation": "Load testing each sprint",
                    "owner": "QA Team"
                }
            ]
        }

        migration_plan = {
            "stories": migration_stories,
            "roadmap": roadmap,
            "approach": "Agile - adjust plan each sprint based on learnings"
        }

        self.architecture_repository['migration_plan'] = migration_plan

        return migration_plan

    # ========================================
    # PHASE H: Architecture Change Management
    # ========================================

    def phase_h_governance_continuous(self) -> Dict:
        """
        Phase H: Architecture Governance

        TOGAF Traditional:
        - Quarterly architecture reviews
        - Change request process (weeks)
        - Heavy compliance checks

        Agile Adaptation:
        - ADRs in每个 sprint
        - Monthly Architecture Board
        - Automated compliance checks
        """

        governance_model = {
            "continuous_activities": {
                "sprint_planning": "Identify architecture decisions needed (ADRs)",
                "sprint_execution": "Make decisions, update ADRs",
                "sprint_review": "Present ADRs to stakeholders",
                "sprint_retro": "Improve decision-making process"
            },
            "monthly_activities": {
                "architecture_board_review": "Review all ADRs from last month",
                "compliance_check": "Verify alignment with principles",
                "metrics_review": "Architecture health metrics",
                "backlog_refinement": "Adjust roadmap based on learnings"
            },
            "quarterly_activities": {
                "architecture_vision_review": "Reassess vision and roadmap",
                "principle_updates": "Update principles if needed",
                "strategic_planning": "Plan next quarter's architecture work"
            },
            "automated_governance": {
                "fitness_functions": [
                    "No service >1000 lines of code per file",
                    "All APIs have OpenAPI spec",
                    "All services have <200ms p95 response time",
                    "Test coverage >80%"
                ],
                "policy_as_code": [
                    "SecurityPolicy: Authentication required",
                    "CostPolicy: Alert if >$5K/month",
                    "CompliancePolicy: PCI-DSS checks"
                ]
            }
        }

        self.architecture_repository['governance'] = governance_model

        return governance_model

# ==========================================
# EJEMPLO: TOGAF ADM Agile End-to-End
# ==========================================

def example_togaf_agile_full_cycle():
    """Ejemplo completo de TOGAF ADM adaptado a Agile"""

    executor = AgileTOGAFPhaseExecutor()

    print("=== TOGAF ADM AGILE ADAPTATION ===\n")

    # Preliminary Phase (2 days)
    print("📋 PRELIMINARY PHASE (2 days)\n")
    charter = executor.preliminary_phase_agile()
    print(f"Architecture Charter created: {charter['architecture_vision']}\n")

    # Phase A: Vision (1 sprint)
    print("🎯 PHASE A: ARCHITECTURE VISION (Sprint 0 - 2 weeks)\n")
    vision_result = executor.phase_a_vision_agile(sprint_duration_weeks=2)
    print(f"Vision created: {len(vision_result['epics'])} epics")
    print(f"Output: {vision_result['output_pages']}\n")

    # Phase B-D: Target Architecture (2 sprints)
    print("🏗️  PHASE B-D: TARGET ARCHITECTURE (Sprints 1-2 - 4 weeks)\n")
    target_arch = executor.phase_b_d_target_architecture_agile()
    print(f"Services defined: {len(target_arch['application']['services'])}")
    print(f"Building blocks: {len(target_arch['building_blocks'])}")
    print(f"Gaps identified: {len(target_arch['gaps'])}\n")

    # Phase E-F: Migration Planning (1 week)
    print("🚀 PHASE E-F: MIGRATION PLANNING (1 week)\n")
    migration = executor.phase_e_f_migration_planning_agile(target_arch)
    print(f"Migration stories: {len(migration['stories'])}")
    print(f"Migration phases: {len(migration['roadmap']['phases'])}\n")

    # Phase H: Governance (Continuous)
    print("⚖️  PHASE H: GOVERNANCE (Continuous)\n")
    governance = executor.phase_h_governance_continuous()
    print(f"Automated fitness functions: {len(governance['automated_governance']['fitness_functions'])}")
    print(f"Policy as code: {len(governance['automated_governance']['policy_as_code'])}\n")

    print("="*60)
    print("TOGAF ADM AGILE ADAPTATION COMPLETE")
    print("="*60)
    print(f"\nTotal duration: ~7 weeks (vs 6+ months traditional)")
    print(f"Output: ~30 pages (vs 200+ pages traditional)")
    print(f"Approach: Iterative & continuous (vs waterfall)")

if __name__ == "__main__":
    example_togaf_agile_full_cycle()
```

---

## 5. Templates y Artefactos

### Template Collection

```markdown
# ==========================================
# TEMPLATE 1: ADR para Sprint Planning
# ==========================================

# ADR-{NUMBER}: {TITLE}

**Fecha:** {YYYY-MM-DD}
**Sprint:** Sprint {NUMBER}
**Estado:** Draft | Proposed | Accepted | Rejected | Superseded
**Nivel de Governance:** Team | Technical | Tactical | Strategic

## Contexto y Problema

**User Story:** {US-ID}: {User story title}

**Problema arquitectónico:**
{¿Qué decisión arquitectónica debemos tomar para implementar esta historia?}

**Ejemplo:**
Para implementar US-101 "Como usuario quiero login con email/password",
necesitamos decidir qué estrategia de autenticación usar.

## Factores de Decisión

Prioridad:
1. ⭐⭐⭐ {Factor crítico 1}
2. ⭐⭐ {Factor importante 2}
3. ⭐ {Factor nice-to-have 3}

## Opciones Consideradas

### Opción 1: {Nombre}

**Descripción:** {Breve descripción}

**Pros:**
- ✅ {Pro 1}
- ✅ {Pro 2}

**Cons:**
- ❌ {Con 1}
- ❌ {Con 2}

**Costo:** ${X}/month or ${Y} one-time
**Complejidad:** Low | Medium | High
**Risk:** Low | Medium | High

### Opción 2: ...

## Decisión

**Elegimos:** {Opción seleccionada}

**Rationale:**
{¿Por qué esta opción es la mejor para nuestro contexto?}

**Implementación:**
{Cómo la vamos a implementar en este sprint}

## Consecuencias

### Positivas ✅
- {Consecuencia positiva 1}
- {Consecuencia positiva 2}

### Negativas ⚠️
- {Consecuencia negativa 1} → Mitigación: {cómo la mitigamos}
- {Consecuencia negativa 2} → Mitigación: {cómo la mitigamos}

### Riesgos 🔥
- {Riesgo 1} → Plan: {contingencia}
- {Riesgo 2} → Plan: {contingencia}

## Compliance con TOGAF Principles

- [ ] Cloud-native first
- [ ] API-first design
- [ ] Security by default
- [ ] Cost-effective

**Notas:** {Explicar cualquier principio que no se cumpla y por qué}

## Stakeholders

**Deciders:** {Quienes toman la decisión}
**Consulted:** {Quienes deben ser consultados}
**Informed:** {Quienes deben ser informados}

## Aprobación

- [ ] Team approval (si governance_level = Team)
- [ ] Tech Lead approval (si governance_level = Technical)
- [ ] Lead Architect approval (si governance_level = Tactical)
- [ ] Architecture Board approval (si governance_level = Strategic)

## Referencias

- Spike results: {link a documentación de spike}
- Related ADRs: {ADR-XXX, ADR-YYY}
- TOGAF phase: {Phase X}
- Epic: {EPIC-ID}

---

# ==========================================
# TEMPLATE 2: TOGAF Architecture Vision (Agile)
# ==========================================

# Architecture Vision - {PROJECT NAME}

**Versión:** 1.0
**Fecha:** {YYYY-MM-DD}
**Autores:** {Architecture Team}
**Stakeholders:** {CTO, Product Owner, etc.}

## Executive Summary (1 paragraph)

{Brief vision statement - what are we building and why}

## Business Drivers

1. **{Driver 1}:** {Description}
   - Metric: {How we measure success}
   - Timeline: {When we need to achieve this}

2. **{Driver 2}:** ...

## Architecture Vision Statement

{2-3 paragraph description of target architecture}

**Example:**
Cloud-native microservices platform on AWS enabling rapid feature delivery
through autonomous teams. Event-driven architecture with Kafka for async
communication. Database per service for independence. Kubernetes for
orchestration and scaling.

## Architecture Principles

1. **{Principle 1}:** {Description}
   - Rationale: {Why this matters}
   - Implications: {What this means for implementation}

2. **Cloud-Native First:**
   - Rationale: Scalability, resilience, managed services
   - Implications: All services deployed as containers on Kubernetes

3. **API-First Design:**
   - Rationale: Enable multiple clients (web, mobile, partners)
   - Implications: OpenAPI specs for all services

## Target Architecture (High-Level)

### Application Architecture
- **Style:** {Microservices | Modular Monolith | etc.}
- **Key Services:** {List of core services}
- **Integration:** {REST APIs | Events | GraphQL}

### Data Architecture
- **Strategy:** {Database per service | Shared database | etc.}
- **Databases:** {PostgreSQL, Redis, etc.}
- **Events:** {Kafka for async communication}

### Technology Architecture
- **Cloud:** {AWS | GCP | Azure}
- **Compute:** {EKS | ECS | Lambda}
- **Observability:** {Prometheus, Grafana, Jaeger}

## Roadmap (Quarterly)

| Quarter | Focus | Key Deliverables |
|---------|-------|------------------|
| Q1 | Foundation | Infrastructure, CI/CD, Core Services |
| Q2 | Features | Business logic, Integrations |
| Q3 | Scale | Performance, Reliability |
| Q4 | Launch | Production release |

## Success Metrics

- [ ] {Metric 1}: {Target}
- [ ] Time to market: < 6 months
- [ ] System availability: > 99.9%
- [ ] Deploy frequency: > 10/day

## Constraints

- **Budget:** ${X}
- **Team Size:** {N} engineers
- **Timeline:** {X} months
- **Compliance:** {PCI-DSS, HIPAA, etc.}

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {Risk 1} | High | High | {Mitigation strategy} |

---

# ==========================================
# TEMPLATE 3: Sprint Planning con ADRs
# ==========================================

# Sprint {NUMBER} Planning

**Date:** {YYYY-MM-DD}
**Duration:** 2 weeks ({Start date} - {End date})
**Team:** {Team members}

## Sprint Goal

{One sentence describing what we want to achieve this sprint}

## Capacity

- Team size: {N} people
- Capacity: {N * 10} story points
- Planned: {X} story points
- Buffer: {Y} story points for unknowns

## User Stories

### Committed

| ID | Title | Points | Architecture Decisions |
|----|-------|--------|------------------------|
| US-101 | User login | 5 | ADR-015: Authentication strategy |
| US-102 | View profile | 3 | ADR-016: Database selection |

### Stretch Goals

{Stories we'll do if we have time}

## Architecture Decisions Needed

### ADR-015: Authentication Strategy

**User Story:** US-101
**Spike:** 4 hours research (Alice)
**Decision Deadline:** Day 3
**Governance Level:** Tactical
**Requires:** Security Team consultation

### ADR-016: Database Selection

**User Story:** US-102
**Spike:** 2 hours research (Bob)
**Decision Deadline:** Day 2
**Governance Level:** Technical
**Requires:** DBA consultation

## Spikes

| Spike | ADR | Assignee | Timebox | Outcome |
|-------|-----|----------|---------|---------|
| Research auth options | ADR-015 | Alice | 4h | Update ADR with 3 options |
| Compare databases | ADR-016 | Bob | 2h | Update ADR with comparison |

## Dependencies

- {Dependency 1}
- ADR-015 must be decided before US-101 implementation can start

## Definition of Done

- [ ] Code written & reviewed
- [ ] Tests passing (unit + integration)
- [ ] ADRs finalized and approved
- [ ] Documentation updated
- [ ] Deployed to staging

---

# ==========================================
# TEMPLATE 4: Architecture Board Review
# ==========================================

# Architecture Board Review - {MONTH} {YEAR}

**Date:** {YYYY-MM-DD}
**Attendees:** {CTO, Lead Architects, etc.}
**Duration:** 2 hours

## ADRs for Review

Total: {N} ADRs from last month

### ADR-{NUMBER}: {TITLE}

**Sprint:** Sprint {X}
**Impact:** {Critical | High | Medium | Low}
**Governance Level:** {Strategic | Tactical}
**Deciders:** {Team/People}

**Decision Summary:**
{Brief summary of the decision}

**Compliance Check:**

| Principle | Compliant? | Notes |
|-----------|------------|-------|
| Cloud-native | ✅ Yes | Uses AWS services |
| API-first | ✅ Yes | OpenAPI spec provided |
| Security | ⚠️ Partial | Needs security review |
| Cost | ❌ No | Exceeds budget |

**Board Decision:**

- [ ] ✅ Approved
- [ ] ⚠️ Approved with conditions: {Conditions}
- [ ] ❌ Rejected: {Reason}
- [ ] 🔄 Request changes: {Changes needed}

**Action Items:**
- {Action 1} - Owner: {Person} - Deadline: {Date}

## Compliance Report

**Overall Compliance:** {X}% of ADRs fully compliant

**Top Violations:**
1. {Violation type}: {N} occurrences
2. {Violation type}: {M} occurrences

## Strategic Recommendations

1. {Recommendation 1}
2. {Recommendation 2}

## Next Month Focus

- {Focus area 1}
- {Focus area 2}

---

# ==========================================
# TEMPLATE 5: Sprint Review ADR Presentation
# ==========================================

# Sprint {NUMBER} Review - Architecture Decisions

**Date:** {YYYY-MM-DD}
**Stakeholders:** {Product Owner, CTO, etc.}

## Sprint Goal Achievement

**Goal:** {Sprint goal}
**Status:** ✅ Achieved | ⚠️ Partially | ❌ Not achieved

## Architecture Decisions Made

### ADR-{NUMBER}: {TITLE}

**Context:** Needed for {User Story}

**Decision:** {What we decided}

**Impact:**
- Performance: {Impact}
- Cost: ${X}/month
- Complexity: {Low/Medium/High}
- Team velocity: {Impact on development speed}

**Status:** ✅ Implemented | ⏸️ Partially implemented

**Demo:** {Link to working demo}

## Escalations to Architecture Board

The following decisions require Board approval:

1. **ADR-{NUMBER}:** {Title}
   - Why: {Exceeds team authority / High cost / etc.}
   - Requested decision by: {Date}

## Stakeholder Feedback Needed

1. **ADR-{NUMBER}:** {Title}
   - Question: {What we need feedback on}

## Lessons Learned

**What went well:**
- {Learning 1}

**What to improve:**
- {Improvement 1}

## Next Sprint Architecture Work

-{Upcoming decisions needed}

```

*File continues with sections 6-10...*
