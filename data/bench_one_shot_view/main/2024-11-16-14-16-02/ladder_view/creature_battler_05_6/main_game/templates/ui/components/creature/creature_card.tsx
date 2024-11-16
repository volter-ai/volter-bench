import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface BaseProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  value?: number
}

let BaseCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let BaseCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let BaseCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let BaseCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let BaseProgress = React.forwardRef<HTMLDivElement, BaseProgressProps>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

BaseCard = withClickable(BaseCard)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)
BaseCardContent = withClickable(BaseCardContent)
BaseProgress = withClickable(BaseProgress)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <BaseCard uid={`${uid}-card`} className={cn("w-[300px]", className)} {...props} ref={ref}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`} className="flex flex-col gap-4">
          <img 
            src={image}
            alt={name}
            className="w-full h-48 object-contain"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <BaseProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
