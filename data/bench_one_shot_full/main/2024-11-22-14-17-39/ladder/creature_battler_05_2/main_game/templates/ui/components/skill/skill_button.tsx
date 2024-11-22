import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    pp?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button uid={`${uid}-button`} ref={ref} {...props}>
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="font-medium leading-none">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
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

export { SkillButton }
