import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, className, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover-card`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button uid={`${uid}-button`} ref={ref} {...props}>
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="font-medium leading-none">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="flex flex-col gap-1 text-sm">
              {stats.damage && <span>Damage: {stats.damage}</span>}
              {stats.accuracy && <span>Accuracy: {stats.accuracy}%</span>}
              {stats.cost && <span>Cost: {stats.cost}</span>}
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
