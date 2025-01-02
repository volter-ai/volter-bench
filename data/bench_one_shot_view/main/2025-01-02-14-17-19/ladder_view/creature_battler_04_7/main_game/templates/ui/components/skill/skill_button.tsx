import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string;
  skillName: string;
  skillDescription: string;
  skillStats: string;
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <button className="skill-button" {...props}>
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
}

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
