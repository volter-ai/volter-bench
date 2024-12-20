import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillHoverCard = withClickable(({ uid, children }: { uid: string, children: React.ReactNode }) => (
  <div>{children}</div>
))

let SkillHoverTrigger = withClickable(({ uid, children, ...props }: { uid: string, children: React.ReactNode } & React.HTMLAttributes<HTMLDivElement>) => (
  <div {...props}>{children}</div>
))

let SkillHoverContent = withClickable(({ uid, children, className, ...props }: { uid: string, children: React.ReactNode, className?: string } & React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md", className)} {...props}>
    {children}
  </div>
))

let SkillButtonBase = withClickable(({ uid, className, ...props }: { uid: string } & React.ButtonHTMLAttributes<HTMLButtonElement>) => (
  <button className={cn("inline-flex items-center justify-center rounded-md text-sm font-medium", className)} {...props} />
))

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, stats, ...props }, ref) => {
    return (
      <SkillHoverCard uid={`${uid}-hover`}>
        <SkillHoverTrigger uid={`${uid}-trigger`}>
          <SkillButtonBase
            ref={ref}
            uid={`${uid}-button`}
            className={cn("w-[200px] justify-start", className)}
            {...props}
          >
            {skillName}
          </SkillButtonBase>
        </SkillHoverTrigger>
        <SkillHoverContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm text-muted-foreground">{description}</p>
            <div className="flex gap-4 text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.type && <div>Type: {stats.type}</div>}
            </div>
          </div>
        </SkillHoverContent>
      </SkillHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

export { SkillButton }
