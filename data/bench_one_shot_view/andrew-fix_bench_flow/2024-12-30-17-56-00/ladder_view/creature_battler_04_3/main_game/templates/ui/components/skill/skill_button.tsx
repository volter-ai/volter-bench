import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable.tsx"

interface SkillButtonProps {
  uid: string
  skillName: string
  skillDescription: string
  skillStats: string
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats }: SkillButtonProps) => (
  <HoverCard>
    <HoverCardTrigger asChild>
      <button className="skill-button">
        {skillName}
      </button>
    </HoverCardTrigger>
    <HoverCardContent>
      <div className="skill-tooltip">
        <h3>{skillName}</h3>
        <p>{skillDescription}</p>
        <p>{skillStats}</p>
      </div>
    </HoverCardContent>
  </HoverCard>
)

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
