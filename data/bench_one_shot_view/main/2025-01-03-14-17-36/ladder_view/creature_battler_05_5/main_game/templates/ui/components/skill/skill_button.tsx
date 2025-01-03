import * as React from "react"
import { Button, ButtonProps } from "@/components/ui/button"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import { withClickable } from '@/lib/withClickable'

interface SkillButtonProps extends ButtonProps {
  uid: string;
  skillName: string;
  description: string;
  stats: string;
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger asChild>
          <Button ref={ref} uid={uid} {...props}>
            {skillName}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid}>
          <div>
            <h3 className="font-bold">{skillName}</h3>
            <p>{description}</p>
            <p>{stats}</p>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"
SkillButton = withClickable(SkillButton)

export { SkillButton }
