import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  imageUrl: string
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <Card ref={ref} className={className} {...props} />
  )
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardHeader ref={ref} className={className} {...props} />
  )
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardContent ref={ref} className={className} {...props} />
  )
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps>(
  ({ className, uid, ...props }, ref) => (
    <CardTitle ref={ref} className={className} {...props} />
  )
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, ...props }, ref) => {
    return (
      <CustomCard uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="flex justify-between items-center">
              <span className="font-bold">HP:</span>
              <span>{hp}</span>
            </div>
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CustomCard.displayName = "CustomCard"
CustomCardHeader.displayName = "CustomCardHeader"
CustomCardContent.displayName = "CustomCardContent"
CustomCardTitle.displayName = "CustomCardTitle"
CreatureCard.displayName = "CreatureCard"

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardContent = withClickable(CustomCardContent)
CustomCardTitle = withClickable(CustomCardTitle)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
