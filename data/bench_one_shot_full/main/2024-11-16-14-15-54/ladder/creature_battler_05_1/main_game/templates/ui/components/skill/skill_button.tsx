import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { withClickable } from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    pp?: number
  }
  onClick?: () => void
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            onClick={onClick}
            uid={`${uid}-button`}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.pp && <div>PP: {stats.pp}</div>}
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
