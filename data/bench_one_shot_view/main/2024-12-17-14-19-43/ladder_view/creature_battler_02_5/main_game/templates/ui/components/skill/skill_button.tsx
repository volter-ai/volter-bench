import * as React from "react"
import { Button } from "@/components/templates/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/templates/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  description?: string
  stats?: string
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, description, stats, children, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={uid} asChild>
          <Button ref={ref} uid={uid} {...props}>
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={uid}>
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <p className="text-sm font-mono">{stats}</p>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
