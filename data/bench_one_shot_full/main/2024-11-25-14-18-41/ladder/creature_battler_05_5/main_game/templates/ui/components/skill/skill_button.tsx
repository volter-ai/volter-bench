import * as React from "react"
import { CustomHoverCard, CustomHoverCardContent, CustomHoverCardTrigger } from "@/components/ui/custom-hover-card"
import { CustomButton } from "@/components/ui/custom-button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

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
      <CustomHoverCard uid={`${uid}-hover`}>
        <CustomHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <CustomButton
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px] h-[50px]", className)}
            {...props}
          >
            {children}
          </CustomButton>
        </CustomHoverCardTrigger>
        <CustomHoverCardContent uid={`${uid}-content`} className="w-80">
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
        </CustomHoverCardContent>
      </CustomHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }
