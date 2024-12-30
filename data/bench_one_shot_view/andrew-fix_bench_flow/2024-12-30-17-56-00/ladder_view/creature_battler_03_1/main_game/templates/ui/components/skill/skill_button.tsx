import * as React from "react"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentPropsWithoutRef<typeof HoverCardTrigger> {
  uid: string
  skillName: string
  skillDescription: string
  skillStats: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, skillDescription, skillStats, ...props }, ref) => (
    <HoverCard>
      <HoverCardTrigger ref={ref} {...props}>
        {skillName}
      </HoverCardTrigger>
      <HoverCardContent>
        <div>
          <h3 className="font-bold">{skillName}</h3>
          <p>{skillDescription}</p>
          <p>{skillStats}</p>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
