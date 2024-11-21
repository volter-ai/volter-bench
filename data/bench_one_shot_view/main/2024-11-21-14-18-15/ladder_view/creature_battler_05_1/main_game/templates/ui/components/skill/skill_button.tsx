import * as React from "react"
import { GameHoverCard, GameHoverCardContent, GameHoverCardTrigger } from "@/components/ui/game/hover-card"
import { GameButton } from "@/components/ui/game/button"
import { cn } from "@/lib/utils"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  description?: string
  stats?: {
    power?: number
    accuracy?: number
    cost?: number
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, children, description, stats, ...props }, ref) => {
    return (
      <GameHoverCard uid={`${uid}-hover`}>
        <GameHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <GameButton
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {children}
          </GameButton>
        </GameHoverCardTrigger>
        <GameHoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            {stats && (
              <div className="text-xs text-muted-foreground">
                {stats.power && <div>Power: {stats.power}</div>}
                {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
                {stats.cost && <div>Cost: {stats.cost}</div>}
              </div>
            )}
          </div>
        </GameHoverCardContent>
      </GameHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
