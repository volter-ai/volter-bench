import * as React from "react"
import { Button, ButtonProps } from "@/components/ui/button"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import { withClickable } from '@/lib/withClickable'

interface SkillButtonProps extends ButtonProps {
  uid: string
  description: string
  stats: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, description, stats, ...props }, ref) => {
    return (
      <HoverCard>
        <HoverCardTrigger asChild>
          <Button ref={ref} {...props} />
        </HoverCardTrigger>
        <HoverCardContent>
          <div>
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
