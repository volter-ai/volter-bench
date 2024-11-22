import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, children, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover-card`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button uid={`${uid}-button`} ref={ref} {...props}>
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            {stats && (
              <div className="text-xs text-muted-foreground">
                {stats.damage && <div>Damage: {stats.damage}</div>}
                {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
                {stats.type && <div>Type: {stats.type}</div>}
              </div>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
