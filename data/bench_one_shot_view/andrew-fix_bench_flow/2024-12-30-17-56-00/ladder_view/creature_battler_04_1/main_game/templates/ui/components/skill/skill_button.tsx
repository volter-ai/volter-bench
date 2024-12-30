import * as React from "react"
import * as HoverCardPrimitive from "@/components/ui/hover-card"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable.tsx"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardPrimitive.Root> {
  uid: string
  skillName: string
  skillDescription: string
  skillStats: string
}

let SkillButton = ({ uid, skillName, skillDescription, skillStats, ...props }: SkillButtonProps) => (
  <HoverCardPrimitive.Root {...props}>
    <HoverCardPrimitive.Trigger asChild>
      <button className="skill-button">{skillName}</button>
    </HoverCardPrimitive.Trigger>
    <HoverCardPrimitive.Content className="skill-tooltip">
      <div className="skill-description">{skillDescription}</div>
      <div className="skill-stats">{skillStats}</div>
    </HoverCardPrimitive.Content>
  </HoverCardPrimitive.Root>
)

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }
