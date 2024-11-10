import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, children, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button uid={`${uid}-button`} ref={ref} {...props}>
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <div className="text-xs text-muted-foreground">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.cost && <div>Cost: {stats.cost}</div>}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
