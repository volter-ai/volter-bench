import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButtonBase = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, disabled, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            onClick={onClick}
            disabled={disabled}
            className="w-full h-full"
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="font-medium">{name}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="grid grid-cols-3 gap-4">
              {stats.damage && (
                <div className="text-sm">
                  <div className="font-medium">Damage</div>
                  <div>{stats.damage}</div>
                </div>
              )}
              {stats.accuracy && (
                <div className="text-sm">
                  <div className="font-medium">Accuracy</div>
                  <div>{stats.accuracy}%</div>
                </div>
              )}
              {stats.cost && (
                <div className="text-sm">
                  <div className="font-medium">Cost</div>
                  <div>{stats.cost}</div>
                </div>
              )}
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButtonBase.displayName = "SkillButton"

let SkillButton = withClickable(SkillButtonBase)

export { SkillButton }
export type { SkillButtonProps }
