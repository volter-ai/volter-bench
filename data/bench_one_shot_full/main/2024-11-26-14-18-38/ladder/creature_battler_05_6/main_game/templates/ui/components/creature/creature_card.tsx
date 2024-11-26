import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

interface CreatureCardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  uid: string
}

interface CreatureProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  value?: number
}

let CreatureCardHeader = React.forwardRef<HTMLDivElement, CreatureCardHeaderProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, CreatureCardContentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, CreatureCardTitleProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CreatureProgress = React.forwardRef<HTMLDivElement, CreatureProgressProps>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl} 
              alt={name}
              className="w-full h-[200px] object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{currentHp}/{maxHp}</span>
              </div>
              <CreatureProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CreatureCardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureProgress.displayName = "CreatureProgress"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureProgress = withClickable(CreatureProgress)

export { 
  CreatureCard,
  CreatureCardHeader,
  CreatureCardContent,
  CreatureCardTitle,
  CreatureProgress
}
