import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/templates/ui/components/hover_card"
import { Button } from "@/templates/ui/components/button"
import { cn } from "@/lib/utils"

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
  ({ className, uid, children, description, stats, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px] h-[50px]", className)}
            {...props}
          >
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            {stats && (
              <div className="text-xs text-muted-foreground">
                {stats.damage && <p>Damage: {stats.damage}</p>}
                {stats.accuracy && <p>Accuracy: {stats.accuracy}%</p>}
                {stats.type && <p>Type: {stats.type}</p>}
              </div>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
