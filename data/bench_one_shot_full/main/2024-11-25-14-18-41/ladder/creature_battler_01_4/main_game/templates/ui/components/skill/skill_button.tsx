import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    healing?: number
    cost?: number
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButtonComponent = React.forwardRef<HTMLDivElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, disabled, className, ...props }, ref) => {
    return (
      <div ref={ref} className={cn(className)} {...props}>
        <HoverCard>
          <HoverCardTrigger asChild>
            <Button 
              onClick={onClick}
              disabled={disabled}
              className="w-[200px]"
            >
              {name}
            </Button>
          </HoverCardTrigger>
          <HoverCardContent className="w-[200px]">
            <div className="space-y-2">
              <h4 className="text-sm font-semibold">{name}</h4>
              <p className="text-sm">{description}</p>
              <div className="text-sm">
                {stats.damage && <div>Damage: {stats.damage}</div>}
                {stats.healing && <div>Healing: {stats.healing}</div>}
                {stats.cost && <div>Cost: {stats.cost}</div>}
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>
      </div>
    )
  }
)

SkillButtonComponent.displayName = "SkillButton"

let SkillButton = withClickable(SkillButtonComponent)

export { SkillButton }
