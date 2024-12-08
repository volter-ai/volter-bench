import * as React from "react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  description: string
  stats: string
}

let SkillButtonBase = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, uid, description, stats, children, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            className={cn("w-[200px]", className)}
            uid={`${uid}-button`}
            {...props}
          >
            {children}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <p className="text-sm text-muted-foreground">{stats}</p>
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButtonBase.displayName = "SkillButton"

let SkillButton = withClickable(SkillButtonBase)

export { SkillButton }
