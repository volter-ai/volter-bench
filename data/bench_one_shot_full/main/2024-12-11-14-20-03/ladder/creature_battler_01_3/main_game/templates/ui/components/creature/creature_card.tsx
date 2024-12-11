import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as BaseCard, CardContent as BaseCardContent, CardHeader as BaseCardHeader, CardTitle as BaseCardTitle } from "@/components/ui/card"
import { Progress as BaseProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface CardProps extends React.ComponentProps<typeof BaseCard> {
  uid: string
}

interface CardContentProps extends React.ComponentProps<typeof BaseCardContent> {
  uid: string
}

interface CardHeaderProps extends React.ComponentProps<typeof BaseCardHeader> {
  uid: string
}

interface CardTitleProps extends React.ComponentProps<typeof BaseCardTitle> {
  uid: string
}

interface ProgressProps extends React.ComponentProps<typeof BaseProgress> {
  uid: string
}

let Card = withClickable(({ uid, ...props }: CardProps) => (
  <BaseCard {...props} />
))

let CardContent = withClickable(({ uid, ...props }: CardContentProps) => (
  <BaseCardContent {...props} />
))

let CardHeader = withClickable(({ uid, ...props }: CardHeaderProps) => (
  <BaseCardHeader {...props} />
))

let CardTitle = withClickable(({ uid, ...props }: CardTitleProps) => (
  <BaseCardTitle {...props} />
))

let Progress = withClickable(({ uid, ...props }: ProgressProps) => (
  <BaseProgress {...props} />
))

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{hp}/{maxHp}</span>
              </div>
              <Progress uid={`${uid}-progress`} value={(hp / maxHp) * 100} />
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
