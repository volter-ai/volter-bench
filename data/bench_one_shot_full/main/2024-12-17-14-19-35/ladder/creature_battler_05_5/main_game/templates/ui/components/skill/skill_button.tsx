import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
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
  ({ uid, name, description, stats, className, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover-card`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            uid={`${uid}-button`}
            className={className}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="font-medium leading-none">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="flex flex-col gap-1 text-sm">
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
