import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  currentHp: number
  maxHp: number
  imageUrl: string
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
  ({ uid, ...props }, ref) => <CardHeader ref={ref} uid={uid} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, CreatureCardContentProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} uid={uid} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, CreatureCardTitleProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} uid={uid} {...props} />
)

let CreatureProgress = React.forwardRef<HTMLDivElement, CreatureProgressProps>(
  ({ uid, ...props }, ref) => <Progress ref={ref} uid={uid} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, currentHp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} uid={uid} className={cn("w-[250px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`} className="grid gap-4">
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
          <div className="flex flex-col gap-2">
            <div className="flex justify-between text-sm">
              <span>HP</span>
              <span>{currentHp}/{maxHp}</span>
            </div>
            <CreatureProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
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
