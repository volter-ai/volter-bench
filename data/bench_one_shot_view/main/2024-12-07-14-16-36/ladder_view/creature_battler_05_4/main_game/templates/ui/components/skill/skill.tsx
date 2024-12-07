import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "./hover_card"
import { cn } from "@/lib/utils"

interface SkillProps extends React.ComponentPropsWithoutRef<typeof HoverCardTrigger> {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
}

let Skill = React.forwardRef<HTMLDivElement, SkillProps>(
  ({ className, uid, name, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger
          ref={ref}
          className={cn(
            "inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90",
            className
          )}
          uid={uid}
          {...props}
        >
          {name}
        </HoverCardTrigger>
        <HoverCardContent uid={uid} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="flex gap-4 text-sm">
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

Skill.displayName = "Skill"

export { Skill }
